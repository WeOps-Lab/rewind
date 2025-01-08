from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.child_config.common import ChildConfigCommon


class ChildConfigViewSet(ViewSet):

    @swagger_auto_schema(
        operation_id="get_child_config",
        operation_summary="获取子配置",
        manual_parameters=[
            openapi.Parameter("object_type", openapi.IN_QUERY, description="对象类型", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter("node_id", openapi.IN_QUERY, description="节点id", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter("data_type", openapi.IN_QUERY, description="采集数据类型", type=openapi.TYPE_STRING, required=True),
        ],
        tags=['ChildConfig']
    )
    @action(detail=False, methods=["get"], url_path="get_child_config")
    def get_child_config(self, request):
        object_type = request.query_params.get('object_type')
        node_id = request.query_params.get('node_id')
        data_type = request.query_params.get('data_type')
        content = ChildConfigCommon(object_type).get_child_config(node_id, data_type)
        return WebUtils.response_success(dict(content=content))

    @swagger_auto_schema(
        operation_id="update_child_config",
        operation_summary="更新子配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "object_type": openapi.Schema(type=openapi.TYPE_STRING, description="对象类型"),
                "node_id": openapi.Schema(type=openapi.TYPE_STRING, description="节点id"),
                "data_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集数据类型"),
                "content": openapi.Schema(type=openapi.TYPE_STRING, description="配置内容"),
            },
            required=["object_type", "node_id", "data_type", "content"]
        ),
        tags=['ChildConfig']
    )
    @action(detail=False, methods=["put"], url_path="update_child_config")
    def update_child_config(self, request):
        object_type = request.data.get('object_type')
        node_id = request.data.get('node_id')
        data_type = request.data.get('data_type')
        content = request.data.get('content')
        ChildConfigCommon(object_type).update_child_config(node_id, data_type, content)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="batch_setting_node_config",
        operation_summary="批量设置节点配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "object_type": openapi.Schema(type=openapi.TYPE_STRING, description="对象类型"),
                "nodes": openapi.Schema(
                    type=openapi.TYPE_ARRAY, description="节点列表",
                    items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, description="节点id"),
                        "configs": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="配置列表"),
                    })
                ),
            },
            required=["object_type", "nodes"]
        ),
        tags=['ChildConfig']
    )
    @action(detail=False, methods=["post"], url_path="batch_setting_node_config")
    def batch_setting_node_config(self, request):
        object_type = request.data.get('object_type')
        nodes = request.data.get('nodes')
        ChildConfigCommon(object_type).batch_setting_node_config(nodes)
        return WebUtils.response_success()
