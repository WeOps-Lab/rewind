from django.contrib import admin
from rest_framework import routers

from apps.knowledge_mgmt.file_knowledge_mgmt.views import FileKnowledgeViewSet
from apps.knowledge_mgmt.knowledge_base_mgmt.views import KnowledgeBaseViewSet
from apps.knowledge_mgmt.knowledge_document_mgmt.views import KnowledgeDocumentViewSet
from apps.knowledge_mgmt.manual_knowledge_mgmt.views import ManualKnowledgeViewSet
from apps.knowledge_mgmt.web_page_knowledge_mgmt.views import WebPageKnowledgeViewSet

admin.site.site_title = "Knowledge Base"
admin.site.site_header = admin.site.site_title
router = routers.DefaultRouter()
router.register(r"knowledge_base", KnowledgeBaseViewSet)
router.register(r"file_knowledge", FileKnowledgeViewSet)
router.register(r"knowledge_document", KnowledgeDocumentViewSet)
router.register(r"web_page_knowledge", WebPageKnowledgeViewSet)
router.register(r"manual_knowledge", ManualKnowledgeViewSet)

urlpatterns = router.urls
