from rest_framework import serializers

from apps.model_provider_mgmt.models import EmbedProvider


class EmbedProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbedProvider
        fields = "__all__"
