from apps.node_mgmt.models.installer import ControllerTask, ControllerTaskNode, CollectorTaskNode, CollectorTask


class InstallerService:
    @staticmethod
    def install_controller(cloud_region_id, work_node, package_version_id, nodes):
        """安装控制器"""
        task_obj = ControllerTask.objects.create(
            cloud_region_id=cloud_region_id,
            work_node=work_node,
            package_version_id=package_version_id,
            type="install",
            status="waiting",
        )
        creates = []
        for node in nodes:
            creates.append(ControllerTaskNode(
                task_id=task_obj.id,
                ip=node["ip"],
                os=node["os"],
                organizations=node["organizations"],
                port=node["port"],
                username=node["username"],
                password=node["password"],
                result={"status": "waiting", "message": ""},
            ))
        ControllerTaskNode.objects.bulk_create(creates, batch_size=100)
        return task_obj.id

    @staticmethod
    def uninstall_controller(cloud_region_id, work_node, nodes):
        """安装控制器"""
        task_obj = ControllerTask.objects.create(
            cloud_region_id=cloud_region_id,
            work_node=work_node,
            type="uninstall",
            status="waiting",
        )
        creates = []
        for node in nodes:
            creates.append(ControllerTaskNode(
                task_id=task_obj.id,
                ip=node["ip"],
                os=node["os"],
                port=node["port"],
                username=node["username"],
                password=node["password"],
                result={"status": "waiting", "message": ""},
            ))
        ControllerTaskNode.objects.bulk_create(creates, batch_size=100)
        return task_obj.id

    @staticmethod
    def install_controller_nodes(task_id):
        """获取控制器安装节点信息"""
        task_nodes = ControllerTaskNode.objects.filter(task_id=task_id)
        result = []
        for task_node in task_nodes:
            result.append(dict(
                ip=task_node.ip,
                os=task_node.os,
                organizations=task_node.organizations,
                port=task_node.port,
                result=task_node.result,
            ))
        return result

    @staticmethod
    def install_collector(collector_package, nodes):
        """安装采集器"""
        task_obj = CollectorTask.objects.create(
            type="install",
            status="waiting",
            collector_package=collector_package,
        )
        creates = []
        for node_id in nodes:
            creates.append(CollectorTaskNode(
                task_id=task_obj.id,
                node_id=node_id,
                status="waiting",
                message="",
            ))
        CollectorTaskNode.objects.bulk_create(creates, batch_size=100)
        return task_obj.id

    @staticmethod
    def install_collector_nodes(task_id):
        """获取采集器安装节点信息"""
        task_nodes = CollectorTaskNode.objects.filter(task_id=task_id)
        result = []
        for task_node in task_nodes:
            result.append(dict(
                node_id=task_node.node_id,
                start_time=task_node.start_time,
                end_time=task_node.end_time,
                status=task_node.status,
                result=task_node.result,
            ))
        return result
