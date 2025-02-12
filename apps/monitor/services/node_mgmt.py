from datetime import datetime, timezone

from apps.monitor.models import MonitorInstance, MonitorInstanceOrganization
from apps.monitor.utils.node_mgmt_api import NodeUtils, FormatChildConfig
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI


class InstanceConfigService:
    @staticmethod
    def get_instance_configs(collect_instance_id, instance_type):
        """获取实例配置"""
        configs = NodeUtils.get_instance_child_config(dict(collect_instance_id=collect_instance_id))

        if instance_type == "os":
            pmq = f'any({{instance_id="{collect_instance_id}", instance_type="{instance_type}"}}) by (instance_id,collect_type,config_type)'
            config_map = {(i["collect_instance_id"], i["collect_type"], i["config_type"]): i for i in configs}
        else:
            pmq = f'any({{instance_id="{collect_instance_id}", instance_type="{instance_type}"}}) by (instance_id,collect_type)'
            config_map = {(i["collect_instance_id"], i["collect_type"]): i for i in configs}

        metrics = VictoriaMetricsAPI().query(pmq, "10m")
        instance_config_map = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = metric_info.get("metric", {}).get("instance_id")
            if not instance_id:
                continue
            agent_id = metric_info.get("metric", {}).get("agent_id")
            collect_type = metric_info.get("metric", {}).get("collect_type")
            config_type = metric_info.get("metric", {}).get("config_type")
            _time = metric_info["value"][0]
            key = (instance_id, collect_type, config_type) if instance_type == "os" else (instance_id, collect_type)
            config_info = {
                "instance_id": instance_id,
                "collect_type": collect_type,
                "config_type": config_type,
                "agent_id": agent_id,
                "time": _time,
            }
            other_config_info = config_map.get(key, {})
            config_info.update(
                config_id=other_config_info.get("id"),
                content=other_config_info.get("content"),
            )
            instance_config_map[key] = config_info

        # 补充未查询到的配置，但是在数据库中存在的配置
        for key, config_info in config_map.items():

            if key not in instance_config_map:
                instance_config_map[key] = {
                    "instance_id": config_info["collect_instance_id"],
                    "collect_type": config_info["collect_type"],
                    "config_type": config_info["config_type"],
                    "agent_id": config_info.get("agents")[0],
                    "time": 0,
                    "config_id": config_info["id"],
                    "content": config_info["content"],
                }

        # 状态计算
        result = []
        for conf_info in instance_config_map.values():
            if conf_info["time"] == 0:
                conf_info["status"] = ""
            else:
                conf_info["status"] = InstanceConfigService.calculation_status(conf_info["time"])
            result.append(conf_info)

        return result

    @staticmethod
    def calculation_status(data_time: int):
        """计算状态"""
        # 获取当前时间时间戳，utc0时区的
        now_timestamp = int(datetime.now(timezone.utc).timestamp())
        # 计算时间差
        time_diff = now_timestamp - data_time
        # 5分钟内正常，1小时内不活跃，1小时以上异常
        if time_diff < 300:
            return "normal"
        elif time_diff < 3600:
            return "inactive"
        else:
            return "unavailable"

    @staticmethod
    def create_monitor_instance_by_node_mgmt(data):
        """创建监控对象实例"""

        # 格式化实例id,将实例id统一为字符串元祖（支持多维度组成的实例id）
        for instance in data["instances"]:
            instance["instance_id"] = str(tuple([instance["instance_id"]]))
            if "interval" not in instance:
                instance["interval"] = "10s"

        # 过滤已存在的实例
        objs = MonitorInstance.objects.filter(id_in=[instance["instance_id"] for instance in data["instances"]])
        instance_set = {obj.id for obj in objs}

        # 格式化实例id,将实例id统一为字符串元祖（支持多维度组成的实例id）
        new_instances, old_instances = [], []
        for instance in data["instances"]:
            if instance["instance_id"] in instance_set:
                old_instances.append(instance)
            else:
                new_instances.append(instance)

        data["instances"] = new_instances

        # 实例更新
        instance_map = {
            instance["instance_id"]: {
                "id": instance["instance_id"],
                "name": instance["instance_name"],
                "interval": instance["interval"],
                "monitor_object_id": data["monitor_object_id"],
                "group_ids": instance["group_ids"],
            }
            for instance in data["instances"]
        }

        old_instance_ids = set(
            MonitorInstance.objects.filter(id__in=list(instance_map.keys())).values_list("id", flat=True))
        creates, assos = [], []
        for instance_id, instance_info in instance_map.items():
            group_ids = instance_info.pop("group_ids")
            for group_id in group_ids:
                assos.append((instance_id, group_id))
            if instance_id not in old_instance_ids:
                creates.append(MonitorInstance(**instance_info))
        MonitorInstance.objects.bulk_create(creates, batch_size=200)
        # 实例组织关联
        old_asso_objs = MonitorInstanceOrganization.objects.filter(monitor_instance_id__in=old_instance_ids)
        old_asso_set = {(asso.monitor_instance_id, asso.organization) for asso in old_asso_objs}
        new_asso_set = set(assos) - old_asso_set
        MonitorInstanceOrganization.objects.bulk_create(
            [MonitorInstanceOrganization(monitor_instance_id=asso[0], organization=asso[1]) for asso in new_asso_set],
            batch_size=200
        )
        # 实例配置关联（node）
        result = FormatChildConfig.collector(data)
        NodeUtils.batch_setting_node_child_config(result)

        if old_instances:
            raise Exception(f"以下实例已存在：{'、'.join([instance['instance_name'] for instance in old_instances])}")
