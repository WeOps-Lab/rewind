from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.models.sidecar import CollectorConfiguration
from apps.node_mgmt.serializers.collector_configuration import (
    CollectorConfigurationSerializer,
    CollectorConfigurationCreateSerializer,
    CollectorConfigurationUpdateSerializer, BulkDeleteConfigurationSerializer, ApplyToNodeSerializer
)
from apps.node_mgmt.filters.collector_configuration import CollectorConfigurationFilter
from apps.node_mgmt.services.collector_configuration import CollectorConfigurationService


class CollectorConfigurationViewSet(mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.ListModelMixin,
                                    GenericViewSet):
    queryset = CollectorConfiguration.objects.all().order_by("-created_at")
    serializer_class = CollectorConfigurationSerializer
    filterset_class = CollectorConfigurationFilter
    search_fields = ['id', 'name']

    @swagger_auto_schema(
        operation_summary="获取采集器配置列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="模糊搜索(id, name)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('cloud_region_id', openapi.IN_QUERY, description="云区域ID", type=openapi.TYPE_INTEGER,
                              required=True),
        ],
        tags=['CollectorConfiguration']
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, dict) and 'items' in response.data:
            response.data['items'] = CollectorConfigurationService.calculate_node_count(response.data['items'])
        else:
            response.data = CollectorConfigurationService.calculate_node_count(response.data)
        return response

    @swagger_auto_schema(
        operation_summary="创建采集器配置",
        tags=['CollectorConfiguration'],
        request_body=CollectorConfigurationCreateSerializer,
    )
    def create(self, request, *args, **kwargs):
        self.serializer_class = CollectorConfigurationCreateSerializer
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="部分更新采集器配置",
        tags=['CollectorConfiguration'],
        request_body=CollectorConfigurationUpdateSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = CollectorConfigurationUpdateSerializer
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="删除采集器配置",
        tags=['CollectorConfiguration']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="批量删除采集器配置",
        request_body=BulkDeleteConfigurationSerializer,
        tags=['CollectorConfiguration']
    )
    @action(methods=['post'], detail=False, url_path='bulk_delete')
    def bulk_delete(self, request):
        serializer = BulkDeleteConfigurationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']
        CollectorConfiguration.objects.filter(id__in=ids).delete()
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_summary="应用指定采集器配置到指定节点",
        request_body=ApplyToNodeSerializer,
        tags=['CollectorConfiguration']
    )
    @action(methods=['post'], detail=False, url_path='apply_to_node')
    def apply_to_node(self, request):
        serializer = ApplyToNodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node_id = serializer.validated_data['node_id']
        collector_configuration_id = serializer.validated_data['collector_configuration_id']
        result, message = CollectorConfigurationService.apply_to_node(node_id, collector_configuration_id)
        if result:
            return WebUtils.response_success()
        else:
            return WebUtils.response_error(error_message=message)
