from apps.node_mgmt.child_config.telegraf.host import HostConfig
from apps.node_mgmt.child_config.telegraf.ipmi import IpmiConfig
from apps.node_mgmt.child_config.telegraf.ping import PingConfig
from apps.node_mgmt.child_config.telegraf.snmp import SnmpConfig
from apps.node_mgmt.child_config.telegraf.trap import TrapConfig
from apps.node_mgmt.child_config.telegraf.web import WebConfig
from apps.node_mgmt.models.sidecar import CollectorConfiguration, ChildConfig


OBJECT_TYPE_MAP = {
    "host": HostConfig.patch_set_node_config,
    "web": WebConfig.patch_set_node_config,
    "ping": PingConfig.patch_set_node_config,
    "ipmi": IpmiConfig.patch_set_node_config,
    "trap": TrapConfig.patch_set_node_config,
    "snmp": SnmpConfig.patch_set_node_config,
}


class ChildConfigCommon:
    def __init__(self, object_type, base_config_name="telegraf_config"):
        self.object_type = object_type
        self.base_config_name = base_config_name

    def get_child_config(self, node_id, data_type):
        """获取节点配置"""
        base_config = CollectorConfiguration.objects.filter(nodes__id=node_id, name=self.base_config_name, is_pre=True).first()
        obj = ChildConfig.objects.filter(collector_config_id=base_config.id, object_type=self.object_type, data_type=data_type).first()
        return obj.content if obj else None

    def update_child_config(self, node_id, data_type, content):
        """更新节点配置"""
        base_config = CollectorConfiguration.objects.filter(nodes__id=node_id, name=self.base_config_name, is_pre=True).first()
        ChildConfig.objects.filter(collector_config_id=base_config.id, object_type=self.object_type, data_type=data_type).update(content=content)

    def batch_setting_node_config(self, nodes):
        """批量设置节点配置"""
        method = OBJECT_TYPE_MAP.get(self.object_type)
        if not method:
            raise ValueError(f"Unsupported object type: {self.object_type}")
        method(nodes)
