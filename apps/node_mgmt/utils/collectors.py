from apps.node_mgmt.models.sidecar import CollectorConfiguration, Collector


class CollectorUtils(object):
    def __init__(self, node):
        self.node = node

    def telegraf_config_init(self):
        """
        初始化telegraf配置文件
        """
        collector_obj = Collector.objects.filter(
            name='telegraf', node_operating_system=self.node.operating_system).first()
        obj = CollectorConfiguration.objects.create(
            name='telegraf_config',
            collector=collector_obj.id,
            config_template='telegraf.conf',
        )
        obj.nodes.add(self.node)
        obj.save()
