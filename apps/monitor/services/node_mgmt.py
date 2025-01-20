from apps.monitor.utils.node_mgmt_api import NodeUtils
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

        metrics = VictoriaMetricsAPI().query(pmq, "1h")
        instance_configs = []
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
            instance_configs.append(config_info)

        return instance_configs
