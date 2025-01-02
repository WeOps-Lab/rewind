from rest_framework import serializers

from apps.knowledge_mgmt.models import WebPageKnowledge


class WebPageKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPageKnowledge
        fields = "__all__"
