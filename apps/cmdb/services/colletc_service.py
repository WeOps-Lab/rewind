# -- coding: utf-8 --
# @File: colletc_service.py
# @Time: 2025/3/3 15:23
# @Author: windyzhao
import urllib.parse
from django.db import transaction

from apps.cmdb.constants import STARGAZER_URL, CollectRunStatusType
from apps.cmdb.services.sync_collect import ProtocolCollect
from apps.core.logger import logger
from apps.core.utils.celery_utils import crontab_format, CeleryUtils
from apps.rpc.node_mgmt import NodeMgmt


class CollectModelService(object):
    TASK = "apps.cmdb.celery_tasks.sync_collect_task"
    NAME = "sync_collect_task"

    @staticmethod
    def format_params(data):
        is_interval, scan_cycle = crontab_format(data["scan_cycle"]["value_type"], data["scan_cycle"]["value"])
        not_required = ["access_point", "ip_range", "instances", "credential", "plugin_id", "params"]
        params = {
            "name": data["name"],
            "task_type": data["task_type"],
            "driver_type": data["driver_type"],
            "model_id": data["model_id"],  # 也就是id
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

    @staticmethod
    def push_butch_node_params(instance):
        """
        格式化调用node的参数 并推送
        """
        node = BaseNodeParams(instance)
        node_params = node.main()
        node_mgmt = NodeMgmt()
        logger.info(f"推送节点参数: {node_params}")
        result = node_mgmt.batch_setting_node_child_config(node_params)
        logger.info(f"推送节点参数结果: {result}")

    @staticmethod
    def delete_butch_node_params(instance):
        """
        格式化调用node的参数 并删除
        """
        node = BaseNodeParams(instance)
        node_params = node.main(operator="delete")
        node_mgmt = NodeMgmt()
        result = node_mgmt.delete_instance_child_config(node_params)
        logger.info(f"删除节点参数结果: {result}")

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

            if not instance.is_k8s:
                cls.push_butch_node_params(instance)

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

            if not instance.is_k8s:
                cls.delete_butch_node_params(instance)
                cls.push_butch_node_params(instance)

        return instance.id

    @classmethod
    def destroy(cls, request, view_self):
        instance = view_self.get_object()
        instance_id = instance.id
        if not instance.is_k8s:
            cls.delete_butch_node_params(instance)
        task_name = f"{cls.NAME}_{instance_id}"
        CeleryUtils.delete_periodic_task(task_name)
        instance.delete()
        return instance_id

    @classmethod
    def collect_controller(cls, instance, data) -> dict:
        """
        任务审批，和数据纳管的逻辑保持一致即可
        """

        try:
            result, format_data = ProtocolCollect(instance, data)
            instance.exec_status = CollectRunStatusType.SUCCESS
        except Exception as err:
            import traceback
            logger.error("==任务审批采集失败== task_id={}, error={}".format(instance.id, traceback.format_exc()))
            result = {}
            format_data = {}
            instance.exec_status = CollectRunStatusType.ERROR

        instance.examine = True
        instance.collect_data = result
        instance.format_data = format_data

        instance.collect_digest = {
            "add": len(format_data.get("add", [])),
            "update": len(format_data.get("update", [])),
            "delete": len(format_data.get("delete", [])),
            "association": len(format_data.get("association", [])),
        }
        instance.save()

        return result


class BaseNodeParams(object):
    def __init__(self, instance):
        self.instance = instance
        self.model_id = instance.model_id
        self.base_path = f"{STARGAZER_URL}/api/collect/collect_info"

    @property
    def model_plugin_name(self):
        """
        获取插件名称
        """
        return "vmware_info"

    @property
    def format_server_path(self):

        """
        格式化服务器的路径
        """
        params = getattr(self, f"{self.model_id}_credential")
        params.update({"plugin_name": self.model_plugin_name})
        encoded_params = {k: urllib.parse.quote(str(v), safe='@') for k, v in params.items()}
        url = f"{self.base_path}?" + "&".join(f"{k}={v}" for k, v in encoded_params.items())
        return url

    @property
    def vmware_vc_credential(self):
        """
        生成vmware vc的凭据
        """
        vc_instance = self.instance.instances[0]
        credential = self.instance.credential
        credential_data = {
            "username": credential.get("username"),
            "password": credential.get("password"),
            "hostname": vc_instance.get("ip_addr"),
            "port": credential.get("port", 443),
            "ssl": str(credential.get("ssl", False)).lower(),
        }
        return credential_data

    @property
    def get_instances(self):
        return self.instance.instances

    @property
    def get_instance_type(self):
        if self.model_id == "vmware_vc":
            instance_type = "vmware"
        else:
            instance_type = self.model_id
        return f"cmdb_{instance_type}"

    def get_vmware_vc_instance_id(self, instance):
        """
        获取实例id
        """
        instance_id = f"{self.instance.id}_{instance['inst_name']}"
        return instance_id

    def vmware_vc_params(self):
        """
        生成vmware vc的参数
        """
        url = self.format_server_path
        params = {
            "object_type": "http",
            "nodes": []
        }

        for node in self.instance.access_point:
            for instance in self.get_instances:
                node_data = {
                    "id": node["id"],
                    "configs": [{
                        "url": url,
                        "type": "http",
                        "instance_id": str(tuple([self.get_vmware_vc_instance_id(instance)])),
                        "interval": 60,
                        "instance_type": self.get_instance_type,
                    }]
                }
                params["nodes"].append(node_data)

        return params

    def vmware_vc_delete_params(self):
        """
        生成vmware vc的删除参数
        """
        params = []

        for instance in self.get_instances:
            params.append(self.get_vmware_vc_instance_id(instance))

        return params

    def main(self, operator="push"):
        """
        主函数
        """
        if operator == "push":
            params = getattr(self, f"{self.model_id}_params")()
        else:
            params = getattr(self, f"{self.model_id}_delete_params")()
        return params
