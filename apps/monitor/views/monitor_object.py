from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.core.utils.web_utils import WebUtils
from apps.monitor.filters.monitor_object import MonitorObjectFilter
from apps.monitor.language.service import SettingLanguage
from apps.monitor.models import MonitorInstance, MonitorPolicy
from apps.monitor.models.monitor_object import MonitorObject
from apps.monitor.serializers.monitor_object import MonitorObjectSerializer
from config.drf.pagination import CustomPageNumberPagination


class MonitorObjectVieSet(viewsets.ModelViewSet):
    queryset = MonitorObject.objects.all()
    serializer_class = MonitorObjectSerializer
    filterset_class = MonitorObjectFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_id="monitor_object_list",
        operation_description="监控对象列表",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        results = serializer.data
        lan = SettingLanguage(request.user.locale)
        for result in results:
            result["display_type"] = lan.get_val("MONITOR_OBJECT_TYPE", result["type"]) or result["type"]
            result["display_name"] = lan.get_val("MONITOR_OBJECT", result["name"]) or result["name"]

        if request.GET.get("add_instance_count") in ["true", "True"]:
            count_data = MonitorInstance.objects.values('monitor_object_id').annotate(instance_count=Count('id'))
            count_map = {i["monitor_object_id"]: i["instance_count"] for i in count_data}
            for result in results:
                result["instance_count"] = count_map.get(result["id"], 0)

        if request.GET.get("add_policy_count") in ["true", "True"]:
            count_data = MonitorPolicy.objects.values('monitor_object_id').annotate(policy_count=Count('id'))
            count_map = {i["monitor_object_id"]: i["policy_count"] for i in count_data}
            for result in results:
                result["policy_count"] = count_map.get(result["id"], 0)

        return WebUtils.response_success(results)

    @swagger_auto_schema(
        operation_id="monitor_object_create",
        operation_description="创建监控对象",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_update",
        operation_description="更新监控对象",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_partial_update",
        operation_description="部分更新监控对象",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_retrieve",
        operation_description="查询监控对象",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="monitor_object_del",
        operation_description="删除监控对象",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     operation_id="monitor_object_import",
    #     operation_description="导入监控对象",
    # )
    # @action(methods=['post'], detail=False, url_path='import')
    # def import_monitor_object(self, request):
    #     MonitorObjectService.import_monitor_object(request.data)
    #     return WebUtils.response_success()
    #
    # @swagger_auto_schema(
    #     operation_id="monitor_object_export",
    #     operation_description="导出监控对象",
    # )
    # @action(methods=['get'], detail=False, url_path='export/(?P<pk>[^/.]+)')
    # def export_monitor_object(self, request, pk):
    #     data = MonitorObjectService.export_monitor_object(pk)
    #     return WebUtils.response_success(data)
