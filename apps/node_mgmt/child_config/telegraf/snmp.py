from string import Template

from apps.node_mgmt.models.sidecar import CollectorConfiguration, ChildConfig

CONFIG_MAP = {
    "switch": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "router": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "firewall": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "loadbalance": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "detection_device": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "scanning_device": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "bastion_host": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "storage": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
    "hardware_server": """[[inputs.snmp]]
    tags = { "instance_id"="${instance_id}", "instance_type"="${instance_type}" }
    ${snmp_config}

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysUpTime.0"
        name = "uptime"

    [[inputs.snmp.field]]
        oid = "RFC1213-MIB::sysName.0"
        name = "source"
        is_tag = true

    [[inputs.snmp.table]]
        oid = "IF-MIB::ifTable"
        name = "interface"
        inherit_tags = ["source"]

    [[inputs.snmp.table.field]]
        oid = "IF-MIB::ifDescr"
        name = "ifDescr"
        is_tag = true""",
}


class SnmpConfig:
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
                    collect_type="snmp",
                    config_type=node_config["type"],
                    content=content,
                    collector_config_id=base_config_id,
                    collect_instance_id=node_config["instance_id"],
                ))

        # 删除已存在的配置
        ChildConfig.objects.filter(collector_config_id__in=base_config_ids, collect_type="snmp").delete()
        # 批量创建节点配置
        ChildConfig.objects.bulk_create(node_objs)
