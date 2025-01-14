from rest_framework import viewsets

from apps.model_provider_mgmt.models import OCRProvider
from apps.model_provider_mgmt.serializers.ocr_serializer import OCRProviderSerializer


class OCRProviderViewSet(viewsets.ModelViewSet):
    queryset = OCRProvider.objects.all()
    serializer_class = OCRProviderSerializer
