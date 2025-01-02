from rest_framework import serializers

from apps.knowledge_mgmt.models import FileKnowledge


class FileKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileKnowledge
        fields = "__all__"
