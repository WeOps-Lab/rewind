from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.monitor.utils.node_mgmt_api import NodeUtils


class NodeMgmtView(ViewSet):
    @swagger_auto_schema(
        operation_description="查询节点列表",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "cloud_region_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="云区域ID"),
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, description="页码"),
                "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="每页数据条数"),
            },
            required=["cloud_region_id", "page", "page_size"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='nodes')
    def get_nodes(self, request):
        organization_ids = [] if request.user.is_superuser else [i["id"] for i in request.user.group_list]
        data = NodeUtils.get_nodes(dict(
            cloud_region_id=request.data.get("cloud_region_id", 1),
            organization_ids=organization_ids,
            name=request.data.get("name"),
            ip=request.data.get("ip"),
            os=request.data.get("os"),
            page=request.data.get("page", 1),
            page_size=request.data.get("page_size", 10),
        ))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="批量设置节点子配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "monitor_object_id": openapi.Schema(type=openapi.TYPE_STRING, description="监控对象id"),
                "collect_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集类型"),
                "configs": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "type": openapi.Schema(type=openapi.TYPE_STRING, description="配置类型"),
                            "...": openapi.Schema(type=openapi.TYPE_STRING, description="配置内容"),
                        }
                    )),
                "instances": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="实例id"),
                            "instance_type": openapi.Schema(type=openapi.TYPE_STRING, description="实例类型"),
                            "instance_name": openapi.Schema(type=openapi.TYPE_STRING, description="实例类型"),
                            "group_ids": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER), description="组织id列表"),
                            "node_ids": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_INTEGER), description="节点id列表"),
                            "...": openapi.Schema(type=openapi.TYPE_OBJECT, description="其他信息"),
                        }
                    )
                )
            },
            required=["monitor_object_id", "collect_type", "configs", "instances"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='batch_setting_node_child_config')
    def batch_setting_node_child_config(self, request):
        data = NodeUtils.batch_setting_node_child_config(request.data)
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询实例子配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "object_type": openapi.Schema(type=openapi.TYPE_STRING, description="对象类型"),
                "collect_type": openapi.Schema(type=openapi.TYPE_STRING, description="采集类型"),
                "config_type": openapi.Schema(type=openapi.TYPE_STRING, description="配置类型"),
                "collect_instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="采集实例ID"),
            },
            required=["object_type", "collect_instance_id"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='get_instance_child_config')
    def get_instance_child_config(self, request):
        data = NodeUtils.get_instance_child_config(dict(
            object_type=request.data.get("object_type"),
            collect_type=request.data.get("collect_type"),
            config_type=request.data.get("config_type"),
            collect_instance_id=request.data.get("collect_instance_id"),
        ))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="更改子配置",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING, description="子配置id"),
                "content": openapi.Schema(type=openapi.TYPE_STRING, description="子配置内容"),
            },
            required=["id", "content"]
        ),
        tags=['NodeMgmt']
    )
    @action(methods=['post'], detail=False, url_path='update_instance_child_config')
    def update_instance_child_config(self, request):
        data = NodeUtils.update_instance_child_config(request.data)
        return WebUtils.response_success(data)
