from apps.node_mgmt.models.cloud_region import CloudRegion


def cloud_init():
    """
    初始化云区域
    """
    CloudRegion.objects.update_or_create(id=1, defaults={"id":1, "name": "默认云区域", "introduction": "默认云区域!"})
