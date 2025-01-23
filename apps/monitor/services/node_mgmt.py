from datetime import datetime, timezone

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
