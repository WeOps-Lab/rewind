from rest_framework import serializers

from apps.model_provider_mgmt.models import LLMModel, LLMSkill
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
