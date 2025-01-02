from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.model_provider_mgmt.models import OCRProvider
from apps.model_provider_mgmt.serializers.ocr_serializer import OCRProviderSerializer


class OCRProviderViewSet(GuardianModelViewSet):
    queryset = OCRProvider.objects.all()
    serializer_class = OCRProviderSerializer
