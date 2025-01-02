from celery import shared_task
from django.conf import settings
from langserve import RemoteRunnable
from tqdm import tqdm

from apps.core.logger import celery_logger as logger
from apps.core.utils.elasticsearch_utils import get_es_client
from apps.knowledge_mgmt.models import (
    FileKnowledge,
    KnowledgeBase,
    KnowledgeDocument,
    ManualKnowledge,
    WebPageKnowledge,
)
from apps.knowledge_mgmt.models.knowledge_document import DocumentStatus


@shared_task
def general_embed(knowledge_document_id_list):
    logger.info(f"general_embed: {knowledge_document_id_list}")
    document_list = KnowledgeDocument.objects.filter(id__in=knowledge_document_id_list)
    general_embed_by_document_list(document_list)
    logger.info(f"knowledge training finished: {knowledge_document_id_list}")


@shared_task
def retrain_all(knowledge_base_id):
    logger.info("Start retraining")
    knowledge_base = KnowledgeBase.objects.get(id=knowledge_base_id)
    knowledge_base.recreate_es_index()
    document_list = KnowledgeDocument.objects.filter(knowledge_base_id=knowledge_base_id)
    document_list.update(train_status=DocumentStatus.CHUNKING)
    general_embed_by_document_list(document_list)


def general_embed_by_document_list(document_list, is_show=False):
    if is_show:
        remote_docs = invoke_one_document(document_list[0])
        docs = [i.page_content for i in remote_docs][:10]
        return docs
    for index, document in tqdm(enumerate(document_list)):
        invoke_document_to_es.delay(document.id)


@shared_task
def invoke_document_to_es(document_id):
    document = KnowledgeDocument.objects.filter(id=document_id).first()
    if not document:
        logger.error(f"document {document_id} not found")
        return
    es_client = get_es_client()
    remote_indexer = RemoteRunnable(settings.REMOTE_INDEX_URL)
    document.train_status = DocumentStatus.CHUNKING
    document.chunk_size = 0
    document.train_progress = 0
    document.save()
    logger.info(f"document {document.name} progress: {document.train_progress}")
    document.delete_es_content(es_client)
    knowledge_docs = invoke_one_document(document)
    if not knowledge_docs:
        document.train_status = DocumentStatus.ERROR
        document.save()
        return
    document.train_status = DocumentStatus.TRAINING
    document.train_progress = 0
    document.save()
    logger.info(f"document {document.name} progress: {document.train_progress}")
    splice_docs = [knowledge_docs[i : i + 100] for i in range(0, document.chunk_size, 100)]
    splice_count = len(splice_docs)
    process_num = round(98 / splice_count, 4)
    for docs in splice_docs:
        invoke_to_es_by_splice(docs, document, process_num, remote_indexer)
    document.train_status = DocumentStatus.READY
    document.train_progress = 100
    document.save()
    logger.info(f"document {document.name} progress: {document.train_progress}")
    es_client.transport.close()


def invoke_to_es_by_splice(docs, document, process_num, remote_indexer):
    try:
        remote_indexer.invoke(
            {
                "elasticsearch_url": settings.ELASTICSEARCH_URL,
                "elasticsearch_password": settings.ELASTICSEARCH_PASSWORD,
                "embed_model_address": document.knowledge_base.embed_model.embed_config["base_url"],
                "index_name": document.knowledge_base.knowledge_index_name(),
                "index_mode": "",
                "docs": docs,
            }
        )
    except Exception as e:
        logger.exception(e)
        document.train_status = DocumentStatus.ERROR
        document.train_progress = 0
        document.save()
        return
    document.train_progress = round(document.train_progress + process_num, 4)
    document.save()
    logger.info(f"document {document.name} process: {document.train_progress}")


def invoke_one_document(document):
    source_invoke_format_map = {
        "file": format_file_invoke_kwargs,
        "manual": format_manual_invoke_kwargs,
        "web_page": format_web_page_invoke_kwargs,
    }
    remote_url_map = {
        "file": RemoteRunnable(settings.FILE_CHUNK_SERVICE_URL),
        "manual": RemoteRunnable(settings.MANUAL_CHUNK_SERVICE_URL),
        "web_page": RemoteRunnable(settings.WEB_PAGE_CHUNK_SERVICE_URL),
    }

    knowledge_docs = []
    source_type = document.knowledge_source_type
    source_remote = remote_url_map[source_type]
    logger.info("Start handle {} knowledge: {}".format(source_type, document.name))
    kwargs = format_invoke_kwargs(document, source_type)
    kwargs.update(source_invoke_format_map[source_type](document))
    try:
        remote_docs = source_remote.invoke(kwargs)
        document.chunk_size = len(remote_docs)
        knowledge_docs.extend(remote_docs)
    except Exception as e:
        logger.exception(e)
    return knowledge_docs


def format_file_invoke_kwargs(document):
    knowledge = FileKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "file_name": document.name,
        "file": knowledge.get_file_base64(),
    }


def format_manual_invoke_kwargs(document):
    knowledge = ManualKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "content": document.name + knowledge.content,
    }


def format_web_page_invoke_kwargs(document):
    knowledge = WebPageKnowledge.objects.filter(knowledge_document_id=document.id).first()
    return {
        "url": knowledge.url,
        "max_depth": knowledge.max_depth,
    }


def format_invoke_kwargs(knowledge_document: KnowledgeDocument, knowledge_source_type):
    semantic_embedding_address = ""
    if knowledge_document.semantic_chunk_parse_embedding_model:
        semantic_embedding_address = knowledge_document.semantic_chunk_parse_embedding_model.embed_config["base_url"]
    ocr_provider_address = ""
    if knowledge_document.ocr_model:
        ocr_provider_address = knowledge_document.ocr_model.ocr_config["base_url"]
    return {
        "enable_recursive_chunk_parse": knowledge_document.enable_general_parse,
        "recursive_chunk_size": knowledge_document.general_parse_chunk_size,
        "recursive_chunk_overlap": knowledge_document.general_parse_chunk_overlap,
        "enable_semantic_chunk_parse": knowledge_document.enable_semantic_chunk_parse,
        "enable_ocr_parse": knowledge_document.enable_ocr_parse,
        "semantic_embedding_address": semantic_embedding_address,
        "excel_header_row_parse": knowledge_document.excel_header_row_parse,
        "excel_full_content_parse": knowledge_document.excel_full_content_parse,
        "ocr_provider_address": ocr_provider_address,
        "custom_metadata": {
            "knowledge_type": knowledge_source_type,
            "knowledge_id": knowledge_document.id,
            "knowledge_title": knowledge_document.name,
            "knowledge_base_id": knowledge_document.knowledge_base.id,
            "enabled": True,
        },
    }
