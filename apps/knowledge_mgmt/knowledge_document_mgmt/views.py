from django.db import transaction
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.decorators import action

from apps.bot_mgmt.models import ConversationTag
from apps.core.logger import logger
from apps.core.utils.elasticsearch_utils import get_es_client
from apps.core.utils.viewset_utils import AuthViewSet
from apps.knowledge_mgmt.knowledge_document_mgmt.serializers import KnowledgeDocumentSerializer
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument, ManualKnowledge, WebPageKnowledge
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.knowledge_mgmt.tasks import general_embed, general_embed_by_document_list


class ObjFilter(FilterSet):
    knowledge_base_id = filters.NumberFilter(field_name="knowledge_base_id", lookup_expr="exact")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    knowledge_source_type = filters.CharFilter(field_name="knowledge_source_type", lookup_expr="exact")
    train_status = filters.NumberFilter(field_name="train_status", lookup_expr="exact")


class KnowledgeDocumentViewSet(AuthViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer
    filterset_class = ObjFilter
    ordering = ("-id",)

    @action(methods=["POST"], detail=False)
    def preprocess(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        preview = kwargs.pop("preview", False)
        is_save_only = kwargs.pop("is_save_only", False)
        if preview:
            KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(**kwargs)
            document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_ids)
            doc_list = general_embed_by_document_list(document_list, True)
            return JsonResponse({"result": True, "data": doc_list})
        if not is_save_only:
            if KnowledgeDocument.objects.filter(
                id__in=knowledge_document_ids, train_status=DocumentStatus.TRAINING
            ).exists():
                return JsonResponse({"result": False, "message": _("training document can not be retrained")})
            kwargs["train_status"] = DocumentStatus.TRAINING
        KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(**kwargs)
        if not is_save_only:
            general_embed.delay(knowledge_document_ids)
        return JsonResponse({"result": True})

    def destroy(self, request, *args, **kwargs):
        instance: KnowledgeDocument = self.get_object()
        if instance.train_status == DocumentStatus.TRAINING:
            return JsonResponse({"result": False, "message": _("training document can not be deleted")})
        with transaction.atomic():
            ConversationTag.objects.filter(knowledge_document_id=instance.id).delete()
            instance.delete()
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def batch_train(self, request):
        kwargs = request.data
        knowledge_document_ids = kwargs.pop("knowledge_document_ids", [])
        if type(knowledge_document_ids) is not list:
            knowledge_document_ids = [knowledge_document_ids]
        KnowledgeDocument.objects.filter(id__in=knowledge_document_ids).update(train_status=DocumentStatus.TRAINING)
        general_embed.delay(knowledge_document_ids)
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    def testing(self, request):
        kwargs = request.data
        knowledge_base_id = kwargs.pop("knowledge_base_id", 0)
        query = kwargs.pop("query", "")
        if not query:
            return JsonResponse({"result": False, "message": _("query is required")})

        service = KnowledgeSearchService()
        knowledge_base = KnowledgeBase.objects.get(id=knowledge_base_id)
        docs = service.search(knowledge_base, query, kwargs)
        doc_ids = [doc["knowledge_id"] for doc in docs]
        knowledge_document_list = KnowledgeDocument.objects.filter(id__in=set(doc_ids)).values(
            "id", "name", "knowledge_source_type", "created_by", "created_at"
        )
        doc_map = {doc["id"]: doc for doc in knowledge_document_list}
        for i in docs:
            knowledge_id = i.pop("knowledge_id")
            doc_obj = doc_map.get(knowledge_id)
            if not doc_obj:
                logger.warning(f"knowledge_id: {knowledge_id} not found")
                continue
            i.update(doc_obj)
        return JsonResponse({"result": True, "data": docs})

    @action(methods=["GET"], detail=True)
    def get_detail(self, request, *args, **kwargs):
        instance: KnowledgeDocument = self.get_object()
        es_client = get_es_client()
        search_text = request.GET.get("search_text", "")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"metadata.knowledge_id": instance.id}},
                    ],
                }
            },
            "sort": [{"_doc": {"order": "desc"}}],
            "from": (page - 1) * page_size,
            "size": page_size,
        }
        if search_text:
            query["query"]["bool"]["must"].append({"match": {"text": search_text}})  # noqa
        res = es_client.search(index=instance.knowledge_index_name(), body=query)
        hits = res.get("hits", {}).get("hits", [])
        total_hits = res.get("hits", {}).get("total", {}).get("value", 0)
        es_client.transport.close()
        return JsonResponse(
            {
                "result": True,
                "data": {
                    "items": [{"id": i["_id"], "content": i["_source"]["text"]} for i in hits],
                    "count": total_hits,
                },
            }
        )

    @action(methods=["POST"], detail=True)
    def enable_chunk(self, request, *args, **kwargs):
        instance: KnowledgeDocument = self.get_object()
        enabled = request.data.get("enabled", False)
        chunk_id = request.data.get("chunk_id", "")
        if not chunk_id:
            return JsonResponse({"result": False, "message": _("chunk_id is required")})
        es_client = get_es_client()
        update_body = {"doc": {"metadata": {"enabled": enabled}}}
        try:
            es_client.update(index=instance.knowledge_index_name(), id=chunk_id, body=update_body)
            es_client.transport.close()
            return JsonResponse({"result": True})
        except Exception as e:
            es_client.transport.close()
            logger.exception(e)
            return JsonResponse({"result": False, "message": _("update failed")})

    @action(methods=["POST"], detail=True)
    def delete_chunk(self, request, *args, **kwargs):
        instance: KnowledgeDocument = self.get_object()
        chunk_id = request.data.get("chunk_id", "")
        if not chunk_id:
            return JsonResponse({"result": False, "message": _("chunk_id is required")})
        es_client = get_es_client()
        try:
            res = es_client.delete(index=instance.knowledge_index_name(), id=chunk_id)
            es_client.transport.close()
            return JsonResponse({"result": True, "data": res})
        except Exception as e:
            es_client.transport.close()
            logger.exception(e)
            return JsonResponse({"result": False, "message": _("delete failed")})

    @action(methods=["POST"], detail=False)
    def batch_delete(self, request):
        doc_ids = request.data.get("doc_ids", [])
        knowledge_base_id = request.data.get("knowledge_base_id", 0)
        if KnowledgeDocument.objects.filter(id__in=doc_ids, train_status=DocumentStatus.TRAINING).exists():
            return JsonResponse({"result": False, "message": _("training document can not be deleted")})
        KnowledgeDocument.objects.filter(id__in=doc_ids).delete()
        index_name = f"knowledge_base_{knowledge_base_id}"
        query = {"query": {"terms": {"metadata.knowledge_id": doc_ids}}}
        es_client = get_es_client()
        try:
            es_client.delete_by_query(index=index_name, body=query)
        except Exception as e:
            logger.exception(e)
            return JsonResponse({"result": False, "message": _("delete failed")})
        es_client.transport.close()
        return JsonResponse({"result": True})

    @action(methods=["GET"], detail=True)
    def get_document_detail(self, request, *args, **kwargs):
        obj: KnowledgeDocument = self.get_object()
        result = {"document_id": obj.id, "name": obj.name, "knowledge_source_type": obj.knowledge_source_type}
        knowledge_model_map = {
            "web_page": WebPageKnowledge,
            "manual": ManualKnowledge,
        }
        doc = knowledge_model_map[obj.knowledge_source_type].objects.filter(knowledge_document_id=obj.id).first()
        result.update(doc.to_dict())
        return JsonResponse({"result": True, "data": result})

    @action(methods=["POST"], detail=True)
    def update_document_base_info(self, request, *args, **kwargs):
        obj: KnowledgeDocument = self.get_object()
        knowledge_model_map = {
            "web_page": WebPageKnowledge,
            "manual": ManualKnowledge,
        }
        doc = knowledge_model_map[obj.knowledge_source_type].objects.filter(knowledge_document_id=obj.id).first()
        params = request.data
        name = params.pop("name", "")
        for key, value in params.items():
            setattr(doc, key, value)
        if name:
            obj.name = name
            obj.save()
        doc.save()
        return JsonResponse({"result": True})
