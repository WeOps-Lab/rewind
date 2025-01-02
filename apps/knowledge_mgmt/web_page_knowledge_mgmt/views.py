from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import action

from apps.core.utils.viewset_utils import AuthViewSet
from apps.knowledge_mgmt.knowledge_document_mgmt.utils import KnowledgeDocumentUtils
from apps.knowledge_mgmt.models import WebPageKnowledge
from apps.knowledge_mgmt.web_page_knowledge_mgmt.serializers import WebPageKnowledgeSerializer


class WebPageKnowledgeViewSet(AuthViewSet):
    queryset = WebPageKnowledge.objects.all()
    serializer_class = WebPageKnowledgeSerializer
    ordering = ("-id",)
    search_fields = ("name",)

    @action(methods=["POST"], detail=False)
    def create_web_page_knowledge(self, request):
        kwargs = request.data
        if not kwargs.get("url"):
            return JsonResponse({"result": False, "data": _("url is required")})
        kwargs["knowledge_source_type"] = "web_page"
        new_doc = KnowledgeDocumentUtils.get_new_document(kwargs, request.user.username)
        knowledge_obj = WebPageKnowledge.objects.create(
            knowledge_document_id=new_doc.id,
            url=kwargs.get("url", ""),
            max_depth=kwargs.get("max_depth", 1),
        )
        return JsonResponse({"result": True, "data": knowledge_obj.knowledge_document_id})
