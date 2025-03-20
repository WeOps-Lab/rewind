# -- coding: utf-8 --
# @File: celery_tasks.py
# @Time: 2025/3/3 15:34
# @Author: windyzhao
from datetime import datetime, timedelta

from celery import shared_task

from apps.core.logger import logger
from apps.cmdb.models.collect_model import CollectModels
from apps.cmdb.services.sync_collect import ProtocolCollect
from apps.cmdb.constants import CollectDriverTypes, CollectRunStatusType


@shared_task
def sync_collect_task(instance_id):
    """
    同步采集任务
    """
    instance = CollectModels.objects.get(id=instance_id)
    if instance.exec_status != CollectRunStatusType.RUNNING:
        return

    try:
        if instance.driver_type == CollectDriverTypes.JOB:
            # 脚本采集
            result = {}
            format_data = {}
        else:
            # 插件采集
            collect = ProtocolCollect(task=instance)
            result, format_data = collect.main()

        instance.exec_status = CollectRunStatusType.EXAMINE if instance.input_method else CollectRunStatusType.SUCCESS

    except Exception as err:
        import traceback
        logger.error("==采集失败== task_id={}, error={}".format(instance_id, traceback.format_exc()))
        result = {}
        format_data = {}
        instance.exec_status = CollectRunStatusType.ERROR

    try:
        instance.collect_data = result
        instance.format_data = format_data
        instance.collect_digest = {
            "add": len(format_data.get("add", [])),
            "update": len(format_data.get("update", [])),
            "delete": len(format_data.get("delete", [])),
            "association": len(format_data.get("association", [])),
        }
        instance.save()
    except Exception as err:
        logger.error("==保存采集结果失败== task_id={}, error={}".format(instance_id, err))
        CollectModels.objects.filter(id=instance_id).update(exec_status=CollectRunStatusType.ERROR)


@shared_task
def sync_periodic_update_task_status():
    """
    执行脚本5分钟更新一次脚本结果
    :param :
    :return:
    """
    logger.info("==开始周期执行修改采集状态==")
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    rows = CollectModels.objects.filter(exec_status=CollectRunStatusType.RUNNING,
                                        exec_time__lt=five_minutes_ago).update(
        exec_status=CollectRunStatusType.ERROR)
    logger.info("==开始周期执行修改采集状态完成==, rows={}".format(rows))
