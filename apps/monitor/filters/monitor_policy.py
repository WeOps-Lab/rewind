from django_filters import FilterSet, CharFilter

from apps.core.utils.group import get_group_and_subgroup_ids
from apps.monitor.models.monitor_policy import MonitorPolicy


class MonitorPolicyFilter(FilterSet):
    monitor_object_id = CharFilter(field_name="monitor_object", lookup_expr="exact", label="监控对象")
    name = CharFilter(field_name="name", lookup_expr="icontains", label="策略名称")
    organization = CharFilter(method="filter_by_organization", label="组织ID")

    class Meta:
        model = MonitorPolicy
        fields = ["monitor_object_id", "name", "organization"]

    def filter_by_organization(self, queryset, name, value):
        group_and_subgroup_ids = get_group_and_subgroup_ids(value)
        return queryset.filter(policyorganization__organization__in=group_and_subgroup_ids).distinct()