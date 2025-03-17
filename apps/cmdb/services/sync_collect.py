# -- coding: utf-8 --
# @File: sync_collect.py
# @Time: 2025/3/4 10:31
# @Author: windyzhao
from abc import ABC, abstractmethod

from apps.cmdb.constants import CollectPluginTypes
from apps.cmdb.models.collect_model import CollectModels
from apps.cmdb.collection.k8s.service import MetricsCannula, CollectK8sMetrics, CollectVmwareMetrics


class ProtocolCollect(object):
    def __init__(self, task):
        self.task = task

    def get_instance(self):
        instance = self.task.instances[0] if self.task.instances else None
        return instance

    def format_params(self):
        pass

    def collect_k8s(self):
        data = K8sCollect(self.task.id)()
        return data

    def collect_vmware(self):
        data = VmwareCollect(self.task.id)()
        return data

    def main(self):
        if self.task.task_type == CollectPluginTypes.K8S:
            result = self.collect_k8s()
            return result
        elif self.task.task_type == CollectPluginTypes.VM:
            result = self.collect_vmware()
            return result


class BaseCollect(object):
    COLLECT_PLUGIN = None

    def __init__(self, instance_id):
        self.task = CollectModels.objects.get(id=instance_id)
        self.model_id, self.inst_name, self.organization = self.format_params()

    def format_params(self):
        instance = self.task.instances[0]
        return instance["model_id"], instance["inst_name"], instance["organization"]

    def run(self):
        if self.COLLECT_PLUGIN is None:
            raise NotImplementedError("Please implement the collect plugin")

        metrics_cannula = MetricsCannula(organization=self.organization, inst_name=self.inst_name,
                                         task_id=self.task.id, collect_plugin=self.COLLECT_PLUGIN,
                                         manual=self.task.input_method)

        result = metrics_cannula.collect_controller()
        format_data = self.format_collect_data(result)

        return metrics_cannula.collect_data, format_data

    def search(self):
        pass

    @staticmethod
    def format_collect_data(result):
        format_data = {"add": [], "update": [], "delete": []}
        for value in result.values():
            for operator, datas in value.items():
                for status, data in datas.items():
                    for i in data:
                        _data = {"_status": status}
                        if status == "failed":
                            update_data = i.get("instance_info")
                            _data.update(i["instance_info"])
                        else:
                            update_data = i.get("inst_info")
                        if not update_data:
                            continue
                        _data.update(i["inst_info"])  # TODO 如果有关联的话得补充关联的创建状态和数据
                        format_data[operator].append(_data)

        return format_data

    def restart(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.run()


class K8sCollect(BaseCollect):
    COLLECT_PLUGIN = CollectK8sMetrics


class VmwareCollect(BaseCollect):
    COLLECT_PLUGIN = CollectVmwareMetrics
