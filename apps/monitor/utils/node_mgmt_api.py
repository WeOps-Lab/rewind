from apps.monitor.models import MonitorInstance, MonitorInstanceOrganization
from apps.rpc.node_mgmt import NodeMgmt


class FormatChildConfig:

    @staticmethod
    def collector(data):
        object_type = data["collect_type"]
        configs = data["configs"]
        instances = data["instances"]
        if object_type == "host":
            return FormatChildConfig.format_host(configs, instances)
        elif object_type == "ping":
            return FormatChildConfig.format_ping(instances, configs)

    @staticmethod
    def format_host(configs, instances):
        result = {"object_type": "host", "nodes": []}

        for instance in instances:
            instance_id, instance_type = instance["instance_id"], instance["instance_type"]

            for node_id in instance["nodes"]:
                node_info = {"id": node_id, "configs": []}

                for config in configs:
                    node_info["configs"].append({
                        "type": config["type"],
                        "instance_id": instance_id,
                        "instance_type": instance_type,
                    })

                result["nodes"].append(node_info)

        return result

    @staticmethod
    def format_ping(instances, configs):
        result = {"object_type": "ping", "nodes": []}

        for instance in instances:
            instance_id, instance_type = instance["instance_id"], instance["instance_type"]
            url = instance["url"]

            for node_id in instance["nodes"]:
                node_info = {"id": node_id, "configs": []}

                for config in configs:
                    node_info["configs"].append({
                        "type": config["type"],
                        "instance_id": instance_id,
                        "instance_type": instance_type,
                        "url": url,
                    })

                result["nodes"].append(node_info)

        return result

    @staticmethod
    def format_web(instances, configs):
        pass

    @staticmethod
    def format_trap(instances, configs):
        pass

    @staticmethod
    def format_ipmi(instances, configs):
        result = {"collect_type": "ipmi", "nodes": []}

        for instance in instances:
            instance_id, instance_type = instance["instance_id"], instance["instance_type"]
            ip = instance["ip"]

            for node_id in instance["nodes"]:
                node_info = {"id": node_id, "configs": []}

                for config in configs:
                    node_info["configs"].append({
                        "type": config["type"],
                        "instance_id": instance_id,
                        "instance_type": instance_type,
                        "server": f"{config['username']}:{config['password']}@{config['protocol']}({ip})",
                    })

                result["nodes"].append(node_info)

        return result

    @staticmethod
    def format_snmp(instances, configs):
        pass


class NodeUtils:

    @staticmethod
    def get_nodes(query_data: dict):
        return NodeMgmt().node_list(query_data)

    @staticmethod
    def batch_setting_node_child_config(data: dict):
        # 实例更新
        instance_map = {
            instance["instance_id"]: {
                "id": instance["instance_id"],
                "name": instance["instance_name"],
                "agent_id": instance["agent_id"],
                "monitor_object_id": data["monitor_object_id"],
                "auto": instance["auto"],
                "group_ids": instance["group_ids"],
            }
            for instance in data["instances"]
        }

        old_instance_ids = set(MonitorInstance.objects.filter(agent_id=data["agent_id"]).values_list("id", flat=True))
        creates, assos = [], []
        for instance_id, instance_info in instance_map.items():
            group_ids = instance_info.pop("group_ids")
            for group_id in group_ids:
                assos.append((instance_id, group_id))
            if instance_id not in old_instance_ids:
                creates.append(MonitorInstance(**instance_info))
        MonitorInstance.objects.bulk_create(creates, batch_size=200)
        # 实例组织关联
        old_asso_objs = MonitorInstanceOrganization.objects.filter(instance_id__in=old_instance_ids)
        old_asso_set = {(asso.monitor_instance_id, asso.organization) for asso in old_asso_objs}
        new_asso_set = set(assos) - old_asso_set
        MonitorInstanceOrganization.objects.bulk_create(
            [MonitorInstanceOrganization(instance_id=asso[0], organization=asso[1]) for asso in new_asso_set],
            batch_size=200
        )
        # 实例配置关联（node）
        return NodeMgmt().batch_setting_node_child_config(data)

    @staticmethod
    def get_instance_child_config(query_data: dict):
        return NodeMgmt().get_instance_child_config(query_data)

    @staticmethod
    def update_instance_child_config(data: dict):
        return NodeMgmt().update_instance_child_config(data)
