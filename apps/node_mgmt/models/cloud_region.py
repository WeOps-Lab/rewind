from django.db import models
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class CloudRegion(TimeInfo, MaintainerInfo):
    name = models.CharField(max_length=100, verbose_name="云区域名称")
    introduction = models.TextField(blank=True, verbose_name="云区域介绍")

    class Meta:
        verbose_name = "云区域"
        db_table = "cloud_region"
        verbose_name_plural = "云区域"



