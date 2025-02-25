from apps.core.utils.viewset_utils import AuthViewSet
from apps.model_provider_mgmt.models import OCRProvider
from apps.model_provider_mgmt.serializers.ocr_serializer import OCRProviderSerializer


class OCRProviderViewSet(AuthViewSet):
    queryset = OCRProvider.objects.all()
    serializer_class = OCRProviderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.query_by_groups(request, queryset)
