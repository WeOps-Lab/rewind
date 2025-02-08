from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.cmdb.services.credential import CredentialManage
from apps.core.utils.web_utils import WebUtils


class CredentialViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_id="create_credential",
        operation_description="创建凭据",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "credential_type": openapi.Schema(type=openapi.TYPE_STRING, description="凭据类型"),
                "data": openapi.Schema(type=openapi.TYPE_OBJECT, description="凭据数据"),
            },
            required=["credential_type", "data"],
        ),
    )
    def create(self, request):
        result = CredentialManage.create_credential(
            request.data["credential_type"],
            request.data["data"],
            request.user.username,
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="encryption_field",
        operation_description="获取加密字段值",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="凭据ID"),
                "field": openapi.Schema(type=openapi.TYPE_STRING, description="凭据属性"),
            },
            required=["id", "field"],
        ),
    )
    @action(detail=False, methods=["post"], url_path="encryption_field")
    def encryption_field(self, request):
        data = CredentialManage.get_encryption_field(request.data["id"], request.data["field"])
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_id="credential_list",
        operation_description="查询凭据列表",
        manual_parameters=[
            openapi.Parameter(
                "credential_type",
                openapi.IN_QUERY,
                description="凭据类型",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def list(self, request):
        credential_type = request.GET.get("credential_type")
        result = CredentialManage.credential_list(
            credential_type,
            request.user.username,
            int(request.GET.get("page", 1)),
            int(request.GET.get("page_size", 10)),
        )
        return WebUtils.response_success(result)

    @swagger_auto_schema(
        operation_id="batch_delete_credential",
        operation_description="批量删除凭据",
        manual_parameters=[
            openapi.Parameter("ids", openapi.IN_QUERY, description="凭据Id（多个用逗号隔离）", type=openapi.TYPE_STRING)
        ],
    )
    @action(detail=False, methods=["delete"], url_path="batch_delete")
    def batch_delete_credential(self, request):
        ids = request.GET.get("ids")
        ids = ids.split(",") if ids else []
        CredentialManage.batch_delete_credential([int(i) for i in ids])
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="update_credential",
        operation_description="更新凭据",
        manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, description="凭据id", type=openapi.TYPE_STRING)],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, description="凭据数据"),
    )
    def partial_update(self, request, pk: str):
        CredentialManage.update_credential(int(pk), request.data)
        return WebUtils.response_success()

    @swagger_auto_schema(
        operation_id="setting_credential_inst_assos",
        operation_description="设置凭据与实例的关联",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "credential_id": openapi.Schema(type=openapi.TYPE_STRING, description="凭据ID"),
                "model_id": openapi.Schema(type=openapi.TYPE_STRING, description="凭据ID"),
                "instance_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="实例ID列表"
                ),
            },
            required=["credential_id", "model_id", "instance_ids"],
        ),
    )
    @action(detail=False, methods=["post"], url_path="credential_association_inst")
    def setting_credential_inst_assos(self, request):
        asso = CredentialManage.credential_asso_inst(request.data, request.user.username)
        return WebUtils.response_success(asso)

    @swagger_auto_schema(
        operation_id="instance_association_instance_list",
        operation_description="查询凭据关联实例列表（或实例关联凭据列表）",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "credential_id": openapi.Schema(type=openapi.TYPE_STRING, description="凭据ID"),
                "instance_id": openapi.Schema(type=openapi.TYPE_STRING, description="实例ID"),
            },
            description="credential_id和instance_id二选一",
        ),
    )
    @action(detail=False, methods=["post"], url_path="credential_association_inst_list")
    def credential_asso_inst_list(self, request):
        asso_insts = CredentialManage.credential_asso_inst_list(request.data, request.user.username)
        return WebUtils.response_success(asso_insts)
