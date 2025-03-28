from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.core.utils.web_utils import WebUtils
from apps.node_mgmt.filters.package import PackageVersionFilter
from apps.node_mgmt.models.package import PackageVersion
from apps.node_mgmt.serializers.package import PackageVersionSerializer
from apps.node_mgmt.utils.package import upload_file, delete_file
from config.drf.pagination import CustomPageNumberPagination


class PackageVersionView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = PackageVersion.objects.all()
    serializer_class = PackageVersionSerializer
    filterset_class = PackageVersionFilter
    pagination_class = CustomPageNumberPagination
    swagger_auto_schema(
        tags=['PackageVersion']
    )

    @swagger_auto_schema(
        operation_id="package_list",
        operation_summary="获取包列表",
        manual_parameters=[
            openapi.Parameter('os', openapi.IN_QUERY, description="操作系统", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="包类型(控制器/采集器)", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="节点名称", type=openapi.TYPE_STRING),
            openapi.Parameter('version', openapi.IN_QUERY, description="包版本号", type=openapi.TYPE_STRING),
        ],
        tags=['PackageVersion']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="package_del",
        operation_summary="删除包",
        tags=['PackageVersion']
    )
    def destroy(self, request, *args, **kwargs):
        # 删除文件，成功了再删除数据
        obj = self.get_object()
        delete_file(obj.version)
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="upload_package",
        operation_summary="上传包",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'os': openapi.Schema(type=openapi.TYPE_STRING, description='操作系统'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='包类型(控制器/采集器)'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='节点名称'),
                'version': openapi.Schema(type=openapi.TYPE_STRING, description='包版本号'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='文件'),
            }
        ),
        tags=['PackageVersion']
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 上传文件，成功了再保存数据
        upload_file(request.data)

        self.perform_create(serializer)
        return WebUtils.response_success(serializer.data)
