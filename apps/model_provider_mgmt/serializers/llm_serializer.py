from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from apps.model_provider_mgmt.models.llm_skill import SkillRequestLog, SkillTools
from config.drf.serializers import TeamSerializer


class LLMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMModel
        fields = "__all__"


class LLMSerializer(TeamSerializer):
    rag_score_threshold = serializers.SerializerMethodField()

    class Meta:
        model = LLMSkill
        fields = "__all__"

    @staticmethod
    def get_rag_score_threshold(instance: LLMSkill):
        return [{"knowledge_base": k, "score": v} for k, v in instance.rag_score_threshold_map.items()]


class SkillRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillRequestLog
        fields = "__all__"


class SkillToolsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = SkillTools
        fields = "__all__"

    @staticmethod
    def get_tags(instance):
        return [_(i) for i in instance.tags]
