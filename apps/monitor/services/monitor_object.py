import ast
import uuid

from django.db.models import Prefetch

from apps.monitor.constants import MONITOR_OBJS
from apps.monitor.models.monitor_metrics import Metric
from apps.monitor.models.monitor_object import MonitorInstance, MonitorObject
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI
from apps.monitor.tasks.grouping_rule import sync_instance_and_group

class MonitorObjectService:

    @staticmethod
    def get_instances_by_metric(metric: str, instance_id_keys: list):
        """获取监控对象实例"""
        metrics = VictoriaMetricsAPI().query(metric)
        instance_map = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = str(tuple([metric_info["metric"].get(i) for i in instance_id_keys]))
            if not instance_id:
                continue
            agent_id = metric_info.get("metric", {}).get("agent_id")
            _time = metric_info["value"][0]

            if instance_id not in instance_map:
                instance_map[instance_id] = {"instance_id": instance_id, "agent_id": agent_id, "time": _time}
            else:
                if _time > instance_map[instance_id]["time"]:
                    instance_map[instance_id] = {"instance_id": instance_id, "agent_id": agent_id, "time": _time}

        return instance_map

    @staticmethod
    def get_monitor_instance(monitor_object_id, page, page_size, name, group_ids, is_super, add_metrics=False):
        """获取监控对象实例"""
        start = (page - 1) * page_size
        end = start + page_size
        qs = MonitorInstance.objects.filter(monitor_object_id=monitor_object_id)
        if not is_super:
            qs = qs.filter(monitorinstanceorganization__organization__in=group_ids)
        qs = qs.prefetch_related(Prefetch('monitorinstanceorganization_set', to_attr='organizations'))
        if name:
            qs = qs.filter(name__icontains=name)

        count = qs.count()

        if page_size == -1:
            objs = qs
        else:
            objs = qs[start:end]

        monitor_obj = MonitorObject.objects.filter(id=monitor_object_id).first()
        if not monitor_obj:
            raise ValueError("Monitor object does not exist")
        obj_metric_map = {i["name"]: i for i in MONITOR_OBJS}
        obj_metric_map = obj_metric_map.get(monitor_obj.name)
        if not obj_metric_map:
            raise ValueError("Monitor object default metric does not exist")
        instance_map = MonitorObjectService.get_instances_by_metric(obj_metric_map.get("default_metric", ""), obj_metric_map.get("instance_id_keys"))
        result = []

        for obj in objs:
            result.append({
                "instance_id": obj.id,
                "instance_name": obj.name or obj.id,
                "agent_id": instance_map.get(obj.id, {}).get("agent_id", ""),
                "organization": [i.organization for i in obj.organizations],
                "time": instance_map.get(obj.id, {}).get("time", ""),
            })

        if add_metrics and page_size != -1:
            # 补充实例指标
            instance_id_keys = obj_metric_map["instance_id_keys"]
            instance_ids = []
            for instance_info in result:
                instance_id = ast.literal_eval(instance_info["instance_id"])
                if len(instance_id) != len(instance_id_keys):
                    continue
                instance_ids.append(instance_id)

            query_parts = []
            for i, key in enumerate(instance_id_keys):
                values = "|".join(set(item[i] for item in instance_ids))  # 去重并拼接
                query_parts.append(f'{key}=~"{values}"')

            metrics_obj = Metric.objects.filter(
                monitor_object_id=monitor_object_id, name__in=obj_metric_map.get("supplementary_indicators", []))
            for metric_obj in metrics_obj:
                query = metric_obj.query
                query = query.replace("__$labels__", f"{', '.join(query_parts)}")
                metrics = VictoriaMetricsAPI().query(query)
                _metric_map = {}
                for metric in metrics.get("data", {}).get("result", []):
                    instance_id = str(tuple([metric["metric"].get(i) for i in metric_obj.instance_id_keys]))
                    value = metric["value"][1]
                    _metric_map[instance_id] = value
                for instance in result:
                    instance[metric_obj.name] = _metric_map.get(instance["instance_id"])

        return  dict(count=count, results=result)

    @staticmethod
    def generate_monitor_instance_id(monitor_object_id, monitor_instance_name, interval):
        """生成监控对象实例ID"""
        obj = MonitorInstance.objects.filter(monitor_object_id=monitor_object_id, name=monitor_instance_name).first()
        if obj:
            obj.interval = interval
            obj.save()
            return obj.id
        else:
            # 生成一个uui
            instance_id = uuid.uuid4().hex
            MonitorInstance.objects.create(
                id=instance_id, name=monitor_instance_name, interval=interval, monitor_object_id=monitor_object_id)

            return instance_id

    @staticmethod
    def check_monitor_instance(monitor_object_id, instance_info):
        """创建监控对象实例"""

        instance_id = str(tuple([instance_info["instance_id"]]))
        objs = MonitorInstance.objects.filter(id=instance_id).first()
        if objs:
            raise Exception(f"实例已存在：{instance_info['instance_name']}")
        # if "interval" not in instance_info:
        #     instance_info["interval"] = "10s"
        # MonitorInstance.objects.create(
        #     id=instance_id,
        #     name=instance_info["instance_name"],
        #     interval=instance_info["interval"],
        #     monitor_object_id=monitor_object_id,
        # )


    @staticmethod
    def autodiscover_monitor_instance():
        """同步监控实例数据"""
        sync_instance_and_group.delay()
