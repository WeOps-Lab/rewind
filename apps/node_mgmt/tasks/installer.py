from celery import shared_task

from apps.node_mgmt.models import ControllerTask
from apps.node_mgmt.utils.installer import send_file, exec_command


@shared_task
def install_controller(task_id):
    """安装控制器"""
    task_obj = ControllerTask.objects.filter(id=task_id).first()
    if not task_obj:
        return
    task_obj.status = "running"
    task_obj.save()
    # 获取所有节点
    nodes = task_obj.controllertasknode_set.all()
    for node_obj in nodes:
        try:
            # sidecar下发
            send_file(node_obj.ip, node_obj.port, node_obj.username, node_obj.password, "", "")
            node_obj.sidecar_result = {"send": {"status": "success"}}
            # sidecar启动
            exec_command(node_obj.ip, node_obj.port, node_obj.username, node_obj.password, "")
            node_obj.sidecar_result = {"start": {"status": "success"}}
        except Exception as e:
            if "send" not in node_obj.sidecar_result:
                node_obj.sidecar_result = {"send": {"status": "failed", "message": str(e)}}
            else:
                node_obj.sidecar_result["start"] = {"status": "failed", "message": str(e)}

        try:
            # executor下发
            send_file(node_obj.ip, node_obj.port, node_obj.username, node_obj.password, "", "")
            node_obj.executor_result = {"send": {"status": "success"}}
            # executor启动
            exec_command(node_obj.ip, node_obj.port, node_obj.username, node_obj.password, "")
            node_obj.executor_result = {"start": {"status": "success"}}
        except Exception as e:
            if "send" not in node_obj.executor_result:
                node_obj.executor_result = {"send": {"status": "failed", "message": str(e)}}
            else:
                node_obj.executor_result["start"] = {"status": "failed", "message": str(e)}

        node_obj.save()


@shared_task
def uninstall_controller(nodes):
    """卸载控制器"""
    for node_id in nodes:
        try:
            # sidecar停止
            exec_command(node_id, "", "", "", "")
            # sidecar��除
            exec_command(node_id, "", "", "", "")
        except Exception as e:
            pass
    pass


@shared_task
def restart_controller(nodes):
    """重启控制器"""
    pass


@shared_task
def install_collector(task_id):
    """安装采集器"""
    pass


@shared_task
def uninstall_collector(task_id):
    """卸载采集器"""
    pass
