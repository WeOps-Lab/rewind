from django.db.transaction import atomic
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.elasticsearch_utils import get_es_client
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.viewset_utils import AuthViewSet
from apps.knowledge_mgmt.knowledge_base_mgmt.serializers import KnowledgeBaseSerializer
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.knowledge_mgmt.tasks import retrain_all
from apps.model_provider_mgmt.models import EmbedProvider, RerankProvider


class KnowledgeBaseViewSet(AuthViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @HasRole()
    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", "")
        queryset = KnowledgeBase.objects.filter(name__icontains=name)
        return self.query_by_groups(request, queryset)

    @HasRole()
    def create(self, request, *args, **kwargs):
        params = request.data
        if not params.get("team"):
            return JsonResponse({"result": False, "message": _("The team field is required.")})
        rerank_model = RerankProvider.objects.get(name="bce-reranker-base_v1")
        if "embed_model" not in params:
            params["embed_model"] = EmbedProvider.objects.get(name="FastEmbed(BAAI/bge-small-zh-v1.5)").id
        if KnowledgeBase.objects.filter(name=params["name"]).exists():
            return JsonResponse({"result": False, "message": _("The knowledge base name already exists.")})
        params["created_by"] = request.user.username
        params["rerank_model"] = rerank_model.id
        params["enable_rerank"] = False
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)
        es_client = get_es_client()
        with atomic():
            self.perform_create(serializer)
            index = f"knowledge_base_{serializer.data.get('id')}"
            if not es_client.indices.exists(index=index):
                es_client.indices.create(index=index)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @HasRole()
    def update(self, request, *args, **kwargs):
        instance: KnowledgeBase = self.get_object()
        params = request.data
        if instance.embed_model_id != params["embed_model"]:
            if instance.knowledgedocument_set.filter(train_status=DocumentStatus.TRAINING).exists():
                return JsonResponse(
                    {"result": False, "message": _("The knowledge base is training and cannot be modified.")}
                )
            retrain_all.delay(instance.id)
        return super().update(request, *args, **kwargs)

    @action(methods=["POST"], detail=True)
    @HasRole()
    def update_settings(self, request, *args, **kwargs):
        instance: KnowledgeBase = self.get_object()
        kwargs = request.data
        if kwargs.get("name"):
            if KnowledgeBase.objects.filter(name=kwargs["name"]).exclude(id=instance.id).exists():
                return JsonResponse({"result": False, "message": _("The knowledge base name already exists.")})
            instance.name = kwargs["name"]
        if kwargs.get("introduction"):
            instance.introduction = kwargs["introduction"]
        if kwargs.get("team"):
            instance.team = kwargs["team"]
        instance.enable_vector_search = kwargs["enable_vector_search"]
        instance.vector_search_weight = kwargs["vector_search_weight"]
        instance.enable_text_search = kwargs["enable_text_search"]
        instance.text_search_weight = kwargs["text_search_weight"]
        instance.enable_rerank = kwargs["enable_rerank"]
        instance.rerank_model_id = kwargs["rerank_model"]
        instance.text_search_mode = kwargs["text_search_mode"]
        instance.save()
        return JsonResponse({"result": True})

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        if KnowledgeDocument.objects.filter(knowledge_base_id=kwargs["pk"]).exists():
            return JsonResponse(
                {"result": False, "message": _("This knowledge base contains documents and cannot be deleted.")}
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET"])
    @HasRole()
    def get_teams(self, request):
        if not hasattr(request, "user"):
            token = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[-1]
            client = KeyCloakClient()
            _, user_info = client.token_is_valid(token)
            groups = client.get_user_groups(user_info["sub"], "admin" in user_info["realm_access"]["roles"])
        else:
            groups = request.user.group_list
        return JsonResponse({"result": True, "data": groups})
