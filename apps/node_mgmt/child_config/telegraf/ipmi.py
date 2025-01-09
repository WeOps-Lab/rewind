from string import Template

from apps.node_mgmt.models.sidecar import CollectorConfiguration, ChildConfig

CONFIG_MAP = {
    "ipmi_sensor": """[[inputs.ipmi_sensor]]
    servers = ["${server}"]
    tags = { "instance_id"="${instance_id}","instance_type"="ipmi"}""",
}


class IpmiConfig:
    @staticmethod
    def patch_set_node_config(nodes: list):
        """批量添加节点配置"""
        node_objs, base_config_ids = [], []

        for node in nodes:
            node_id = node["id"]
            node_configs = node["configs"]
            base_config = CollectorConfiguration.objects.filter(nodes__id=node_id, name="telegraf_config",
                                                                is_pre=True).first()
            base_config_id = base_config.id
            base_config_ids.append(base_config_id)
            for node_config in node_configs:

                content = CONFIG_MAP[node_config["type"]]
                template = Template(content)
                content = template.safe_substitute(node_config)
                node_objs.append(ChildConfig(
                    object_type="ipmi",
                    data_type=node_config["type"],
                    content=content,
                    collector_config_id=base_config_id
                ))

        # 删除已存在的配置
        ChildConfig.objects.filter(collector_config_id__in=base_config_ids, object_type="ipmi").delete()
        # 批量创建节点配置
        ChildConfig.objects.bulk_create(node_objs)
