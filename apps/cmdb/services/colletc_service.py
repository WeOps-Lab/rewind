# -- coding: utf-8 --
# @File: colletc_service.py
# @Time: 2025/3/3 15:23
# @Author: windyzhao
import datetime

from django.db import transaction

from apps.cmdb.celery_tasks import sync_collect_task
from apps.cmdb.constants import CollectRunStatusType
from apps.core.utils.celery_utils import crontab_format, CeleryUtils


class CollectModelService(object):
    TASK = "apps.cmdb.celery_tasks.sync_collect_task"
    NAME = "sync_collect_task"

    @staticmethod
    def format_params(data):
        is_interval, scan_cycle = crontab_format(data["scan_cycle"]["value_type"], data["scan_cycle"]["value"])
        not_required = ["access_point", "ip_range", "instances", "credential", "plugin_id"]
        params = {
            "name": data["name"],
            "task_type": data["task_type"],
            "driver_type": data["driver_type"],
            "model_id": data["model_id"],  # 也就是id
            "params": data["params"],
            "timeout": data["timeout"],
            "input_method": data["input_method"],
            "is_interval": is_interval,
            "cycle_value": data["scan_cycle"]["value"],
            "cycle_value_type": data["scan_cycle"]["value_type"],
        }

        for key in not_required:
            if data.get(key):
                params[key] = data[key]

        if is_interval and scan_cycle:
            params["scan_cycle"] = scan_cycle

        return params, is_interval, scan_cycle

    @classmethod
    def create(cls, request, view_self):
        create_data, is_interval, scan_cycle = cls.format_params(request.data)

        with transaction.atomic():
            serializer = view_self.get_serializer(data=create_data)
            serializer.is_valid(raise_exception=True)
            view_self.perform_create(serializer)
            instance = serializer.instance

            # 更新定时任务
            if is_interval:
                task_name = f"{cls.NAME}_{instance.id}"
                CeleryUtils.create_or_update_periodic_task(name=task_name, crontab=scan_cycle, args=[instance.id],
                                                           task=cls.TASK)

        return instance.id

    @classmethod
    def update(cls, request, view_self):
        update_data, is_interval, scan_cycle = cls.format_params(request.data)
        with transaction.atomic():
            instance = view_self.get_object()
            serializer = view_self.get_serializer(instance, data=update_data, partial=True)
            serializer.is_valid(raise_exception=True)
            view_self.perform_update(serializer)

            task_name = f"{cls.NAME}_{instance.id}"
            # 更新定时任务
            if is_interval:
                CeleryUtils.create_or_update_periodic_task(name=task_name, crontab=scan_cycle,
                                                           args=[instance.id], task=cls.TASK)
            else:
                CeleryUtils.delete_periodic_task(task_name)

        return instance.id

    @classmethod
    def destroy(cls, request, view_self):
        instance = view_self.get_object()
        instance_id = instance.id
        task_name = f"{cls.NAME}_{instance_id}"
        CeleryUtils.delete_periodic_task(task_name)
        instance.delete()
        return instance_id