from django_filters import FilterSet, CharFilter, IsoDateTimeFromToRangeFilter, BaseInFilter

from apps.monitor.models.monitor_policy import MonitorAlert


class CommaSeparatedCharInFilter(BaseInFilter, CharFilter):
    def filter(self, qs, value):
        if value:
            if isinstance(value, list):
                return super().filter(qs, value)
            elif isinstance(value, str):
                values = [v.strip() for v in value.split(",") if v.strip()]
                return super().filter(qs, values)
        return qs


class MonitorAlertFilter(FilterSet):
    status_in = CommaSeparatedCharInFilter(field_name="status", lookup_expr="in", label="状态")
    level_in = CommaSeparatedCharInFilter(field_name="level", lookup_expr="in", label="告警级别")
    created_at = IsoDateTimeFromToRangeFilter(field_name="created_at", label="创建时间范围")
    content = CharFilter(field_name="content", lookup_expr="icontains", label="告警内容")

    class Meta:
        model = MonitorAlert
        fields = ["status_in", "level_in", "created_at"]
