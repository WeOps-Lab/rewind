from rest_framework import serializers

from apps.model_provider_mgmt.models import RerankProvider


class RerankProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RerankProvider
        fields = "__all__"
