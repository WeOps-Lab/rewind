from rest_framework import serializers

from apps.model_provider_mgmt.models import OCRProvider


class OCRProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRProvider
        fields = "__all__"
