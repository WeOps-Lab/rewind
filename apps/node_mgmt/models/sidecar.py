import uuid

from django.db import models
from django.db.models import JSONField

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.node_mgmt.models.cloud_region import CloudRegion

OS_TYPE = (
    ("linux", "Linux"),
    ("windows", "Windows"),
)


class Node(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=100, verbose_name="节点ID")
    name = models.CharField(max_length=100, verbose_name="节点名称")
    ip = models.CharField(max_length=30, verbose_name="IP地址")
    operating_system = models.CharField(max_length=50, choices=OS_TYPE, verbose_name="操作系统类型")
    collector_configuration_directory = models.CharField(max_length=200, verbose_name="采集器配置目录")
    metrics = JSONField(default=dict, verbose_name="指标")
    status = JSONField(default=dict, verbose_name="状态")
    tags = JSONField(default=list, verbose_name="标签")
    log_file_list = JSONField(default=list, verbose_name="日志文件列表")
    cloud_region = models.ForeignKey(CloudRegion, default=1, on_delete=models.CASCADE, verbose_name="云区域")

    class Meta:
        verbose_name = "节点信息"
        db_table = "node"
        verbose_name_plural = "节点信息"


class NodeOrganization(TimeInfo, MaintainerInfo):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name="节点")
    organization = models.CharField(max_length=100, verbose_name="组织id")

    class Meta:
        verbose_name = "节点组织"
        db_table = "node_organization"
        verbose_name_plural = "节点组织"
        unique_together = ('node', 'organization')


class Collector(TimeInfo, MaintainerInfo):
    ServiceType = (
        ("exec", "执行任务"),
        ("svc", "服务"),
    )

    id = models.CharField(primary_key=True, max_length=100, verbose_name="采集器ID")
    name = models.CharField(max_length=100, verbose_name="采集器名称")
    service_type = models.CharField(max_length=100, choices=ServiceType, verbose_name="服务类型")
    node_operating_system = models.CharField(max_length=50, choices=OS_TYPE, verbose_name="节点操作系统类型")
    executable_path = models.CharField(max_length=200, verbose_name="可执行文件路径")
    execute_parameters = models.CharField(max_length=200, verbose_name="执行参数")
    validation_parameters = models.CharField(blank=True, null=True, max_length=200, verbose_name="验证参数")
    default_template = models.TextField(blank=True, null=True, verbose_name="默认模板")
    introduction = models.TextField(blank=True, verbose_name="采集器介绍")

    class Meta:
        verbose_name = "采集器信息"
        db_table = "collector"
        verbose_name_plural = "采集器信息"


class CollectorConfiguration(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=100, verbose_name="配置ID")
    name = models.CharField(max_length=100, verbose_name="配置名称")
    config_template = models.TextField(blank=True, verbose_name="配置模板")
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE, verbose_name="采集器")
    nodes = models.ManyToManyField(Node, blank=True, verbose_name="节点")
    cloud_region = models.ForeignKey(CloudRegion, default=1, on_delete=models.CASCADE, verbose_name="云区域")

    class Meta:
        verbose_name = "采集器配置信息"
        db_table = "collector_configuration"
        verbose_name_plural = "采集器配置信息"

    # uuid
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)


class Action(TimeInfo, MaintainerInfo):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name="节点")
    action = JSONField(default=list, verbose_name="操作")

    class Meta:
        verbose_name = "操作信息"
        db_table = "action"
        verbose_name_plural = "操作信息"


class SidecarApiToken(TimeInfo, MaintainerInfo):
    token = models.CharField(max_length=100, verbose_name="Token")

    class Meta:
        verbose_name = "Sidecar API Token"
        db_table = "sidecar_api_token"
        verbose_name_plural = "Sidecar API Token"


class SidecarEnv(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    description = models.TextField(blank=True, verbose_name="描述")
    cloud_region = models.ForeignKey(CloudRegion, default=1, on_delete=models.CASCADE, verbose_name="云区域")

    class Meta:
        verbose_name = "Sidecar环境变量"
        db_table = "sidecar_env"
        verbose_name_plural = "Sidecar环境变量"
        unique_together = ('key', 'cloud_region')
