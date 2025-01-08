from apps.node_mgmt.models.sidecar import CollectorConfiguration, ChildConfig

CONFIG_MAP = {

    "cpu":"""[[inputs.cpu]]
    percpu = true
    totalcpu = true
    collect_cpu_time = false
    report_active = false
    core_tags = false
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "disk": """[[inputs.disk]]
    ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "diskio": """[[inputs.diskio]]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "mem": """[[inputs.mem]]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "net": """[[inputs.net]]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "processes": """[[inputs.processes]]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",

    "system": """[[inputs.system]]
    tags = { "instance_id"="${node.id}","instance_type"="os" }""",
}

class HostConfig:
    @staticmethod
    def patch_set_node_config(nodes: list):
        """批量添加节点配置"""
        node_objs, base_config_ids = [], []

        for node in nodes:
            node_id = node["id"]
            node_configs = node["configs"]
            base_config = CollectorConfiguration.objects.filter(nodes__id=node_id, name="telegraf_config", is_pre=True).first()
            base_config_id = base_config.id
            base_config_ids.append(base_config_id)
            for node_config in node_configs:
                content = CONFIG_MAP[node_config]
                node_objs.append(ChildConfig(
                    object_type="host",
                    data_type=node_config,
                    content=content,
                    collector_config_id=base_config_id
                ))

        # 删除已存在的配置
        ChildConfig.objects.filter(collector_config_id__in=base_config_ids, object_type="host").delete()
        # 批量创建节点配置
        ChildConfig.objects.bulk_create(node_objs)
