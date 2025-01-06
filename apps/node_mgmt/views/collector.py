from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.node_mgmt.filters.collector import CollectorFilter
from apps.node_mgmt.models.sidecar import Collector
from apps.node_mgmt.serializers.collector import CollectorSerializer


class CollectorViewSet(mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filterset_class = CollectorFilter
    search_fields = ['id', 'name', 'introduction']

    @swagger_auto_schema(
        operation_summary="获取采集器列表",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="模糊搜索(id, name, introduction)",
                              type=openapi.TYPE_STRING),
        ],
        tags=['Collector']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
