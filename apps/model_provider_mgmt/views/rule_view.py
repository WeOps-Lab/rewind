from django_filters import filters
from django_filters.rest_framework import FilterSet

from apps.core.utils.viewset_utils import AuthViewSet
from apps.model_provider_mgmt.models import SkillRule
from apps.model_provider_mgmt.serializers.rule_serializer import RuleSerializer


class ObjFilter(FilterSet):
    skill_id = filters.NumberFilter(field_name="skill_id", lookup_expr="exact")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class RuleViewSet(AuthViewSet):
    serializer_class = RuleSerializer
    queryset = SkillRule.objects.all()
    filterset_class = ObjFilter
