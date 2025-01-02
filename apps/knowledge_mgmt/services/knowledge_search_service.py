from typing import List

from django.conf import settings
from langserve import RemoteRunnable

from apps.model_provider_mgmt.models import EmbedProvider, RerankProvider


class KnowledgeSearchService:
    @staticmethod
    def search(knowledge_base_folder, query, kwargs, score_threshold=0) -> List[dict]:
        docs = []
        remote_indexer = RemoteRunnable(settings.RAG_SERVER_URL)

        embed_model_address = EmbedProvider.objects.get(id=kwargs["embed_model"]).embed_config["base_url"]
        rerank_model_address = ""

        if kwargs["enable_rerank"]:
            rerank_model_address = RerankProvider.objects.get(id=kwargs["rerank_model"]).rerank_config["base_url"]
        params = {
            "elasticsearch_url": settings.ELASTICSEARCH_URL,
            "elasticsearch_password": settings.ELASTICSEARCH_PASSWORD,
            "embed_model_address": embed_model_address,
            "index_name": knowledge_base_folder.knowledge_index_name(),
            "search_query": query,
            "metadata_filter": {"enabled": True},
            "rag_k": kwargs["rag_k"],  # 返回结果数量
            "rag_num_candidates": kwargs["rag_num_candidates"],  # 候选数量
            "enable_rerank": kwargs["enable_rerank"],
            "rerank_model_address": rerank_model_address,
            "rerank_top_k": 10,  # Rerank返回结果数量
            "enable_text_search": kwargs["enable_text_search"],
            "enable_vector_search": kwargs["enable_vector_search"],
            "text_search_mode": kwargs["text_search_mode"],
        }
        if kwargs["enable_text_search"]:
            params["text_search_weight"] = kwargs["text_search_weight"]
        if kwargs["enable_vector_search"]:
            params["vector_search_weight"] = kwargs["vector_search_weight"]
        result = remote_indexer.invoke(params)
        for doc in result:
            score = doc.metadata["_score"] * 10
            if score <= score_threshold:
                continue

            doc_info = {
                "content": doc.page_content,
                "score": score,
                "knowledge_id": doc.metadata["_source"]["metadata"]["knowledge_id"],
                "knowledge_title": doc.metadata["_source"]["metadata"]["knowledge_title"],
            }
            if kwargs["enable_rerank"]:
                doc_info["rerank_score"] = doc.metadata["relevance_score"]
            docs.append(doc_info)
        docs.sort(key=lambda x: x["score"], reverse=True)
        return docs
