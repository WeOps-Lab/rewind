from celery import shared_task

from apps.node_mgmt.constants import CONTROLLER_INSTALL_DIR, COLLECTOR_INSTALL_DIR, UNZIP_RUN_COMMAND, SIDECAR_API_URL, \
    LINUX_OS
from apps.node_mgmt.models import ControllerTask, CollectorTask, PackageVersion
from apps.node_mgmt.utils.installer import download_to_remote, exec_command_to_remote, download_to_local, \
    exec_command_to_local
from apps.node_mgmt.utils.token_auth import generate_token
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

    # 获取控制器下发目录
    controller_install_dir = CONTROLLER_INSTALL_DIR.get(package_obj.os)

    # 生成解压并执行命令
    unzip_run_command = UNZIP_RUN_COMMAND.get(package_obj.os)
    sidecar_token = generate_token({"username": "admin"})
    unzip_run_command = unzip_run_command.format(package_name=package_obj.name, server_url=SIDECAR_API_URL, server_token=sidecar_token)

    for node_obj in nodes:
        try:
            # 控制器压缩包下发
            download_to_remote(
                task_obj.work_node,
                NATS_NAMESPACE,
                file_key,
                package_obj.name,
                controller_install_dir,
                node_obj.ip,
                node_obj.username,
                node_obj.password,
            )
            node_obj.result.update(send={"status": "success"})
            # 解压包，并执行运行脚步
            exec_command_to_remote(task_obj.work_node, node_obj.ip, node_obj.username, node_obj.password, unzip_run_command)
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

    # 获取采集器下发目录
    collector_install_dir = COLLECTOR_INSTALL_DIR.get(package_obj.os)

    # 获取所有节点
    nodes = task_obj.collectortasknode_set.all()
    for node_obj in nodes:
        try:
            # 下发采集器
            download_to_local(
                node_obj.node_id,
                NATS_NAMESPACE,
                file_key,
                package_obj.name,
                collector_install_dir,
            )
            node_obj.result.update(send={"status": "success"})
            # Linux操作系统赋予执行权限
            if package_obj.os in LINUX_OS:
                exec_command_to_local(node_obj.node_id, f"chmod +x {collector_install_dir}/{package_obj.name}")
                node_obj.result.update(set_exe={"status": "success"})
            else:
                node_obj.result.update(set_exe={"status": "success"})
        except Exception as e:
            node_obj.result.update(send={"status": "failed", "message": str(e)})

        node_obj.save()

    # 更新任务状态
    task_obj.status = "finished"
    task_obj.save()


@shared_task
def uninstall_collector(task_id):
    """卸载采集器"""
    pass
