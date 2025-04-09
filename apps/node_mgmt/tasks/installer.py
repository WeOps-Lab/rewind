from celery import shared_task

from apps.node_mgmt.models import ControllerTask, CollectorTask, PackageVersion
from apps.node_mgmt.utils.installer import send_file, exec_command, download_to_remote, exec_command_to_remote, \
    download_to_local
from config.components.nats import NATS_NAMESPACE


@shared_task
def install_controller(task_id):
    """安装控制器"""
    task_obj = ControllerTask.objects.filter(id=task_id).first()
    if not task_obj:
        raise ValueError("Task not found")
    package_obj = PackageVersion.objects.filter(id=task_obj.package_version_id).first()
    if not package_obj:
        raise ValueError("Package version not found")
    file_key = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
    task_obj.status = "running"
    task_obj.save()

    # 获取所有节点
    nodes = task_obj.controllertasknode_set.all()
    for node_obj in nodes:
        try:
            # 控制器压缩包下发
            download_to_remote(
                task_obj.work_node,
                NATS_NAMESPACE,
                file_key,
                package_obj.name,
                "/home/sidecar",
                node_obj.ip,
                node_obj.username,
                node_obj.password,
            )
            node_obj.result.update(send={"status": "success"})
            # 解压包，并执行运行脚步
            exec_command_to_remote(task_obj.work_node, node_obj.ip, node_obj.username, node_obj.password, "")
            node_obj.result.update(run={"status": "success"})
        except Exception as e:
            if "send" not in node_obj.result:
                node_obj.result.update(send={"status": "failed", "message": str(e)})
            elif "run" not in node_obj.result:
                node_obj.result.update(run={"status": "failed", "message": str(e)})

        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def uninstall_controller(task_id):
    """卸载控制器"""

    task_obj = ControllerTask.objects.filter(id=task_id).first()
    if not task_obj:
        return
    task_obj.status = "running"
    task_obj.save()

    # 获取所有节点
    nodes = task_obj.controllertasknode_set.all()
    for node_obj in nodes:
        try:
            # 执行卸载脚步
            exec_command_to_remote(task_obj.work_node, node_obj.ip, node_obj.username, node_obj.password, "")
            node_obj.result.update(run={"status": "success"})

        except Exception as e:
            node_obj.result.update(run={"status": "failed", "message": str(e)})

        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def install_collector(task_id):
    """安装采集器"""
    task_obj = CollectorTask.objects.filter(id=task_id).first()
    if not task_obj:
        raise ValueError("Task not found")
    package_obj = PackageVersion.objects.filter(id=task_obj.package_version_id).first()
    if not package_obj:
        raise ValueError("Package version not found")
    file_key = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
    task_obj.status = "running"
    task_obj.save()

    # 获取所有节点
    nodes = task_obj.collectortasknode_set.all()
    for node_obj in nodes:
        # 下发采集器
        try:
            download_to_local(
                node_obj.node_id,
                NATS_NAMESPACE,
                file_key,
                package_obj.name,
                "/home/sidecar",
            )
            node_obj.result.update(send={"status": "success"})
        except Exception as e:
            node_obj.result.update(send={"status": "failed", "message": str(e)})

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def uninstall_collector(task_id):
    """卸载采集器"""
    pass
