import json

from django.conf import settings
from django.utils.translation import gettext as _
from langserve import RemoteRunnable

from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMModel, TokenConsumption


class LLMService:
    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, kwargs: dict):
        llm_model = LLMModel.objects.get(id=kwargs["llm_model"])
        context = ""
        title_map = doc_map = {}
        citing_knowledge = []
        if kwargs["enable_rag"]:
            context, title_map, doc_map = self.search_doc(context, kwargs)
        chat_server = RemoteRunnable(settings.OPENAI_CHAT_SERVICE_URL)
        chat_kwargs = {
            "system_message_prompt": kwargs["skill_prompt"],
            "openai_api_base": llm_model.decrypted_llm_config["openai_base_url"],
            "openai_api_key": llm_model.decrypted_llm_config["openai_api_key"],
            "temperature": kwargs["temperature"],
            "model": llm_model.decrypted_llm_config["model"],
            "user_message": kwargs["user_message"],
            "chat_history": kwargs["chat_history"],
            "conversation_window_size": kwargs["conversation_window_size"],
            "rag_context": context,
        }
        result = chat_server.invoke(chat_kwargs)
        if type(result) == str:
            result = json.loads(result)
        if not result["result"]:
            raise Exception(result["message"])
        data = result["data"]
        if "bot_id" in kwargs:
            TokenConsumption.objects.create(
                bot_id=kwargs["bot_id"],
                input_tokens=data["input_tokens"],
                output_tokens=data["output_tokens"],
                username=kwargs["username"],
                user_id=kwargs["user_id"],
            )
        if kwargs["enable_rag_knowledge_source"]:
            citing_knowledge = [
                {
                    "knowledge_title": doc_map.get(k, {}).get("name"),
                    "knowledge_id": k,
                    "knowledge_base_id": doc_map.get(k, {}).get("knowledge_base_id"),
                    "result": v,
                    "knowledge_source_type": doc_map.get(k, {}).get("knowledge_source_type"),
                    "citing_num": len(v),
                }
                for k, v in title_map.items()
            ]
        return {"content": data["content"], "citing_knowledge": citing_knowledge}

    def search_doc(self, context, kwargs):
        title_map = {}
        score_threshold_map = {i["knowledge_base"]: i["score"] for i in kwargs["rag_score_threshold"]}
        base_ids = list(score_threshold_map.keys())
        knowledge_base_list = KnowledgeBase.objects.filter(id__in=base_ids)
        doc_list = list(
            KnowledgeDocument.objects.filter(knowledge_base_id__in=base_ids).values(
                "id", "knowledge_source_type", "name", "knowledge_base_id"
            )
        )
        doc_map = {i["id"]: i for i in doc_list}
        for i in knowledge_base_list:
            params = {
                "enable_rerank": i.enable_rerank,
                "embed_model": i.embed_model.id,
                "rerank_model": i.rerank_model_id,
                "rag_k": i.rag_k,
                "rag_num_candidates": i.rag_num_candidates,
                "enable_text_search": i.enable_text_search,
                "text_search_weight": i.text_search_weight,
                "enable_vector_search": i.enable_vector_search,
                "vector_search_weight": i.vector_search_weight,
                "text_search_mode": i.text_search_mode,
            }
            score_threshold = score_threshold_map.get(i.id, 0.7)
            rag_result = self.knowledge_search_service.search(
                i, kwargs["user_message"], params, score_threshold=score_threshold
            )
            context += _(
                """
The following is the background knowledge provided to you. The format of the background knowledge is as follows:
--------
Knowledge Title: [Title]
Knowledge Content: [Content]
--------

             """
            )
            for r in rag_result:
                context += "--------\n"
                context += _("Knowledge Title:[{}]\n").format(r["knowledge_title"])
                context += _("Knowledge Content:[{}]\n").format(r["content"].replace("{", "").replace("}", ""))
                title_map.setdefault(r["knowledge_id"], []).append(
                    {
                        "content": r["content"],
                        "score": r["score"],
                    }
                )
        return context, title_map, doc_map


llm_service = LLMService()
