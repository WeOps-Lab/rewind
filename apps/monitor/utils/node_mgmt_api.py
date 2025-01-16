from apps.monitor.models import MonitorInstance
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
        return NodeMgmt().batch_setting_node_child_config(data)

    @staticmethod
    def get_instance_child_config(query_data: dict):
        return NodeMgmt().get_instance_child_config(query_data)

    @staticmethod
    def update_instance_child_config(data: dict):
        return NodeMgmt().update_instance_child_config(data)
