from django.db import models
from django.utils.translation import gettext_lazy as _
from elasticsearch import Elasticsearch, NotFoundError

from apps.core.logger import logger
from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from apps.core.utils.elasticsearch_utils import get_es_client


class DocumentStatus(object):
    TRAINING = 0
    READY = 1
    ERROR = 2
    PENDING = 3
    CHUNKING = 4

    CHOICE = (
        (TRAINING, _("Training")),
        (READY, _("Ready")),
        (ERROR, _("Error")),
        (PENDING, _("Pending")),
        (CHUNKING, _("Chunking")),
    )


class KnowledgeDocument(MaintainerInfo, TimeInfo):
    knowledge_base = models.ForeignKey("KnowledgeBase", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True, verbose_name=_("name"))
    chunk_size = models.IntegerField(default=0, verbose_name=_("chunk size"))
    train_status = models.IntegerField(default=0, choices=DocumentStatus.CHOICE, verbose_name=_("train status"))
    train_progress = models.FloatField(default=0, verbose_name=_("train progress"))
    enable_general_parse = models.BooleanField(default=True, verbose_name=_("enable general parse"))
    general_parse_chunk_size = models.IntegerField(default=256, verbose_name=_("general parse chunk size"))
    general_parse_chunk_overlap = models.IntegerField(default=32, verbose_name=_("general parse chunk overlap"))
    enable_semantic_chunk_parse = models.BooleanField(default=False, verbose_name=_("enable semantic chunk parse"))
    semantic_chunk_parse_embedding_model = models.ForeignKey(
        "model_provider_mgmt.EmbedProvider",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("embedding model"),
    )
    enable_ocr_parse = models.BooleanField(default=False, verbose_name=_("enable OCR parse"))
    ocr_model = models.ForeignKey(
        "model_provider_mgmt.OCRProvider", blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("OCR model")
    )
    enable_excel_parse = models.BooleanField(default=True, verbose_name=_("enable Excel parse"))
    excel_header_row_parse = models.BooleanField(default=False, verbose_name=_("Excel header row parse"))
    excel_full_content_parse = models.BooleanField(default=True, verbose_name=_("Excel full content parse"))
    knowledge_source_type = models.CharField(max_length=20, verbose_name=_("source type"), default="file")

    def __str__(self):
        return self.name

    def knowledge_index_name(self):
        return self.knowledge_base.knowledge_index_name()

    def delete_es_content(self, es_client: Elasticsearch):
        index_name = self.knowledge_base.knowledge_index_name()
        query = {"query": {"term": {"metadata.knowledge_id": self.id}}}
        try:
            es_client.delete_by_query(index=index_name, body=query)
            logger.info(_("Document {} successfully deleted.").format(self.name))
        except NotFoundError:
            logger.info(_("Document {} not found, skipping deletion.").format(self.name))

    def delete(self, *args, **kwargs):
        es_client = get_es_client()
        self.delete_es_content(es_client)
        es_client.transport.close()
        return super().delete(*args, **kwargs)  # 调用父类的delete方法来执行实际的删除操作

    class Meta:
        verbose_name = _("Knowledge Document")
        verbose_name_plural = verbose_name
