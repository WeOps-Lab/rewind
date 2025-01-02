from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.model_provider_mgmt.models import EmbedProvider
from apps.model_provider_mgmt.serializers.embed_serializer import EmbedProviderSerializer
from apps.model_provider_mgmt.services.remote_embeddings import RemoteEmbeddings


class EmbedProviderViewSet(GuardianModelViewSet):
    serializer_class = EmbedProviderSerializer
    queryset = EmbedProvider.objects.all()
    search_fields = ["name"]


class EmbedViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=False)
    def embed_content(self, request):
        embed_model_id = request.data.get("embed_model_id")
        content = request.data.get("content")
        embed_provider = EmbedProvider.objects.get(id=embed_model_id)
        embedding_service = RemoteEmbeddings(embed_provider)
        result = embedding_service.embed_query(content)
        return JsonResponse({"embedding": result})
