from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.monitor.utils.node_mgmt_api import NodeApi


class NodeMgmtView(ViewSet):
    @swagger_auto_schema(
        operation_description="查询节点列表",
        manual_parameters=[
            openapi.Parameter("cloud_region_id", openapi.IN_QUERY, description="云区域ID", type=openapi.TYPE_INTEGER,
                              required=False),
            openapi.Parameter("page", openapi.IN_QUERY, description="页码", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="每页数据条数", type=openapi.TYPE_INTEGER,
                              required=False),
        ],
        tags=['NodeMgmt']
    )
    @action(methods=['get'], detail=False, url_path='nodes')
    def get_nodes(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        cloud_region_id = request.GET.get("cloud_region_id", 1)
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 999)
        data = NodeApi(token).get_nodes(cloud_region_id, page, page_size, request.user.is_superuser,
                                        request.user.group_list)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询采集器列表",
        tags=['NodeMgmt']
    )
    @action(methods=['get'], detail=False, url_path='collectors')
    def get_collectors(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        data = NodeApi(token).get_collectors()
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询采集器配置详情",
        manual_parameters=[
            openapi.Parameter("collector_id", openapi.IN_PATH, description="采集器id", type=openapi.TYPE_INTEGER,
                              required=True),
        ],
        tags=['NodeMgmt']
    )
    @action(methods=['get'], detail=False, url_path='config_detail/(?P<config_id>[^/.]+)')
    def config_detail(self, request, config_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        data = NodeApi(token).get_config_detail(config_id)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="创建采集器配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "cloud_region_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="配置信息"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="采集器ID"),
                "collector_id": openapi.Schema(type=openapi.TYPE_STRING, description="配置信息"),
                "config_template": openapi.Schema(type=openapi.TYPE_STRING, description="配置信息"),
                "node_id": openapi.Schema(type=openapi.TYPE_STRING, description="节点id"),
            },
            required=["cloud_region_id", "name", "collector_id", "config_template", "node_id"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='create_config')
    def create_collector_config(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        data = NodeApi(token).create_config(request.data)
        NodeApi(token).node_asso_config(request.data.get("node_id"), data.get("id"))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="更新采集器配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="采集器ID"),
                "config_template": openapi.Schema(type=openapi.TYPE_STRING, description="配置信息"),
            },
            required=["name", "config_template"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='update_config/(?P<config_id>[^/.]+)')
    def update_config(self, request, config_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        data = NodeApi(token).update_config(config_id, request.data)
        return WebUtils.response_success(data)
