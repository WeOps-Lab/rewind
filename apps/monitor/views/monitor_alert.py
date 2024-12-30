from datetime import datetime, timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.utils.web_utils import WebUtils
from apps.monitor.language.service import SettingLanguage
from apps.monitor.models import MonitorAlert, MonitorEvent, MonitorPolicy, MonitorInstance, MonitorObject
from apps.monitor.filters.monitor_alert import MonitorAlertFilter
from apps.monitor.serializers.monitor_alert import MonitorAlertSerializer
from apps.monitor.serializers.monitor_instance import MonitorInstanceSerializer
from apps.monitor.serializers.monitor_metrics import MetricSerializer
from apps.monitor.serializers.monitor_policy import MonitorPolicySerializer
from config.drf.pagination import CustomPageNumberPagination


class MonitorAlertVieSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = MonitorAlert.objects.all().order_by("-created_at")
    serializer_class = MonitorAlertSerializer
    filterset_class = MonitorAlertFilter
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        # 如果不是超管还没有传递组织ID就抛错
        if not request.user.is_superuser and not request.query_params.get('organization'):
            raise ValueError('organization is empty')
        # 获取分页参数
        page = int(request.GET.get('page', 1))  # 默认第1页
        page_size = int(request.GET.get('page_size', 10))  # 默认每页10条数据

        # 获取经过过滤器处理的数据
        queryset = self.filter_queryset(self.get_queryset())

        # 计算分页的起始位置
        start = (page - 1) * page_size
        end = start + page_size

        # 获取当前页的数据
        page_data = queryset[start:end]

        # 执行序列化
        serializer = self.get_serializer(page_data, many=True)
        results = serializer.data

        # 获取当前页中所有的 policy_id 和 monitor_instance_id
        policy_ids = [alert["policy_id"] for alert in results if alert["policy_id"]]
        instance_ids = [alert["monitor_instance_id"] for alert in results if alert["monitor_instance_id"]]

        # 查询所有相关的策略和实例
        policies = MonitorPolicy.objects.filter(id__in=policy_ids).select_related("metric")
        instances = MonitorInstance.objects.filter(id__in=instance_ids)

        # 将策略和实例数据映射到字典中
        policy_dict = {policy.id: policy for policy in policies}
        instance_dict = {instance.id: instance for instance in instances}

        metrics = {policy.metric.id: policy.metric for policy in policies}
        monitor_object_name = None
        lan = SettingLanguage(request.user.locale)
        # 补充策略和实例到每个 alert 中
        for alert in results:
            # 在 results 字典中添加完整的 policy 和 monitor_instance 信息
            alert["policy"] = MonitorPolicySerializer(policy_dict.get(alert["policy_id"])).data if alert[
                "policy_id"] else None
            alert["monitor_instance"] = MonitorInstanceSerializer(
                instance_dict.get(alert["monitor_instance_id"])).data if alert["monitor_instance_id"] else None
            alert["metric"] = MetricSerializer(metrics.get(alert["policy"]["metric"])).data if alert["policy"] else None
            # 翻译指标名称和描述
            if monitor_object_name is None:
                monitor_object = MonitorObject.objects.filter(id=alert["policy"]["monitor_object"]).first()
                if monitor_object:
                    monitor_object_name = monitor_object.name
            if monitor_object_name:
                metric_map = lan.get_val("MONITOR_OBJECT_METRIC", monitor_object_name)
                if not metric_map:
                    metric_map = {}
                alert["metric"]["display_name"] = metric_map.get(alert["metric"]["name"], {}).get("name") or alert["metric"]["name"]
                alert["metric"]["display_description"] = metric_map.get(alert["metric"]["name"], {}).get("desc") or alert["metric"]["description"]

        # 返回成功响应
        return WebUtils.response_success(dict(count=queryset.count(), results=results))


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 检查是否要更新 status 和其他字段
        updated_data = serializer.validated_data
        if updated_data.get("status") == "closed":
            updated_data["end_event_time"] = datetime.now(timezone.utc)  # 补充时间
            updated_data["operator"] = request.user.username  # 假设操作人从请求中获取

        self.perform_update(serializer)

        # 清理缓存
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MonitorEventVieSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="查询告警事件",
        manual_parameters=[
            openapi.Parameter("alert_id", openapi.IN_PATH, description="告警id", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter("page", openapi.IN_QUERY, description="页码", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="每页数量", type=openapi.TYPE_INTEGER, required=False),
        ],
    )
    @action(methods=['get'], detail=False, url_path='query/(?P<alert_id>[^/.]+)')
    def get_events(self, request, alert_id):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        alert_obj = MonitorAlert.objects.get(id=alert_id)
        event_query = dict(
            policy_id=alert_obj.policy_id,
            monitor_instance_id=alert_obj.monitor_instance_id,
            created_at__gte=alert_obj.start_event_time,
        )
        if alert_obj.end_event_time:
            event_query["created_at__lte"] = alert_obj.end_event_time
        q_set = MonitorEvent.objects.filter(**event_query).order_by("-created_at")
        events = q_set[(page - 1) * page_size: page * page_size]
        result = [
            {
                "id": i.id,
                "level": i.level,
                "value": i.value,
                "content": i.content,
                "created_at": i.created_at,
                "monitor_instance_id": i.monitor_instance_id,
                "policy_id": i.policy_id,
            }
            for i in events
        ]
        return WebUtils.response_success(dict(count=q_set.count(), results=result))
