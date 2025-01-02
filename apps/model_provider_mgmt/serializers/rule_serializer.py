from rest_framework import serializers

from apps.model_provider_mgmt.models import SkillRule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillRule
        fields = "__all__"
