from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.utils.web_utils import WebUtils

from apps.monitor.services.metrics import Metrics as MetricsService


class MetricsInstanceVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="查询指标信息",
        manual_parameters=[
            openapi.Parameter("query", openapi.IN_QUERY, description="指标查询参数", type=openapi.TYPE_STRING, required=True),
        ],
    )
    @action(methods=['get'], detail=False, url_path='query')
    def get_metrics(self, request):
        data = MetricsService.get_metrics(request.GET.get('query'))
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询指标信息",
        manual_parameters=[
            openapi.Parameter("query", openapi.IN_QUERY, description="指标查询参数", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter("start", openapi.IN_QUERY, description="开始时间（utc时间戳）", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter("end", openapi.IN_QUERY, description="结束时间（utc时间戳）", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter("step", openapi.IN_QUERY, description="指标采集间隔（eg: 5s）", type=openapi.TYPE_STRING, required=True),
        ],
        required=["query"]
    )
    @action(methods=['get'], detail=False, url_path='query_range')
    def get_metrics_range(self, request):
        data = MetricsService.get_metrics_range(
            request.GET.get('query'),
            request.GET.get('start'),
            request.GET.get('end'),
            request.GET.get('step'),
        )
        return WebUtils.response_success(data)
