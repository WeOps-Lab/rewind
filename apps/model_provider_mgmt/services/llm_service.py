import base64
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from django.conf import settings
from django.utils.translation import gettext as _
from langserve import RemoteRunnable

from apps.base.models.quota_rule import TeamTokenUseInfo
from apps.core.logger import logger
from apps.knowledge_mgmt.models import KnowledgeBase, KnowledgeDocument
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from apps.model_provider_mgmt.models import LLMModel, TokenConsumption


class LLMService:
    """服务类，用于处理与LLM模型交互的逻辑，包括聊天、知识检索等功能"""

    def __init__(self):
        self.knowledge_search_service = KnowledgeSearchService()

    def chat(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理聊天请求，并返回带引用知识的回复内容

        Args:
            kwargs: 包含聊天所需参数的字典

        Returns:
            包含回复内容和引用知识的字典
        """
        citing_knowledge = []
        data, doc_map, title_map = self.invoke_chat(kwargs)

        # 记录token消耗
        if "bot_id" in kwargs:
            TokenConsumption.objects.create(
                bot_id=kwargs["bot_id"],
                input_tokens=data["input_tokens"],
                output_tokens=data["output_tokens"],
                username=kwargs["username"],
                user_id=kwargs["user_id"],
            )

        # 如果启用了知识源引用，构建引用信息
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

    @staticmethod
    def _process_user_message_and_images(user_message: Union[str, List[Dict[str, Any]]]) -> Tuple[str, List[str]]:
        """
        处理用户消息和图片数据

        Args:
            user_message: 用户消息，可能是字符串或包含文本和图片的列表

        Returns:
            处理后的文本消息和图片URL列表
        """
        image_data = []
        text_message = user_message

        if isinstance(user_message, list):
            for item in user_message:
                if item["type"] == "image_url":
                    image_url = item.get("image_url", {}).get("url") or item.get("url")
                    if image_url:
                        image_data.append(image_url)
                else:
                    text_message = item["text"]

        return text_message, image_data

    def _process_chat_history(self, chat_history: List[Dict[str, Any]], window_size: int) -> List[Dict[str, Any]]:
        """
        处理聊天历史，处理窗口大小和图片数据

        Args:
            chat_history: 原始聊天历史
            window_size: 对话窗口大小

        Returns:
            处理后的聊天历史
        """
        num = window_size * -1
        processed_history = []

        for user_msg in chat_history[num:]:
            if user_msg["event"] == "user" and isinstance(user_msg["text"], list):
                image_list = []
                msg = ""
                for item in user_msg["text"]:
                    if item["type"] == "image_url":
                        image_url = item.get("image_url", {}).get("url") or item.get("url")
                        if image_url:
                            image_list.append(image_url)
                    else:
                        msg = item["text"]
                processed_history.append({"event": "user", "text": msg, "image_data": image_list})
            else:
                txt = user_msg["text"]
                if isinstance(txt, list):
                    txt = "\n".join([i["text"] for i in txt])
                processed_history.append({"event": user_msg["event"], "text": txt})

        return processed_history

    def format_stream_chat_params(self, kwargs: Dict[str, Any]) -> Tuple[Dict, Dict, TeamTokenUseInfo, Dict]:
        """
        格式化流式聊天所需的参数

        Args:
            kwargs: 包含聊天所需参数的字典

        Returns:
            文档映射、标题映射、团队令牌使用信息和聊天参数
        """
        llm_model = LLMModel.objects.get(id=kwargs["llm_model"])
        # 处理用户消息和图片
        chat_kwargs, doc_map, title_map = self.format_chat_server_kwargs(kwargs, llm_model)
        # 获取或创建团队令牌使用信息
        group = llm_model.consumer_team or llm_model.team[0]
        team_info, _ = TeamTokenUseInfo.objects.get_or_create(
            group=group, llm_model=llm_model.name, defaults={"used_token": 0}
        )

        return doc_map, title_map, team_info, chat_kwargs

    def format_chat_server_kwargs(self, kwargs, llm_model):
        context = ""
        title_map = doc_map = {}

        # 如果启用RAG，搜索文档
        if kwargs["enable_rag"]:
            context, title_map, doc_map = self.search_doc(context, kwargs)

        user_message, image_data = self._process_user_message_and_images(kwargs["user_message"])
        # 处理聊天历史
        chat_history = self._process_chat_history(kwargs["chat_history"], kwargs["conversation_window_size"])
        # 构建聊天参数
        chat_kwargs = {
            "system_message_prompt": kwargs["skill_prompt"],
            "openai_api_base": llm_model.decrypted_llm_config["openai_base_url"],
            "openai_api_key": llm_model.decrypted_llm_config["openai_api_key"],
            "temperature": kwargs["temperature"],
            "model": llm_model.decrypted_llm_config["model"],
            "user_message": user_message,
            "chat_history": chat_history,
            "conversation_window_size": kwargs["conversation_window_size"],
            "rag_context": context,
            "tools": kwargs.get("tools", []),
            "image_data": image_data,
        }
        return chat_kwargs, doc_map, title_map

    def invoke_chat(self, kwargs: Dict[str, Any]) -> Tuple[Dict, Dict, Dict]:
        """
        调用聊天服务并处理结果

        Args:
            kwargs: 包含聊天所需参数的字典

        Returns:
            处理后的数据、文档映射和标题映射
        """
        chat_server = RemoteRunnable(settings.OPENAI_CHAT_SERVICE_URL)
        show_think = kwargs.pop("show_think", True)
        llm_model = LLMModel.objects.get(id=kwargs["llm_model"])

        # 处理用户消息和图片
        chat_kwargs, doc_map, title_map = self.format_chat_server_kwargs(kwargs, llm_model)

        # 调用聊天服务
        result = chat_server.invoke(chat_kwargs)
        if isinstance(result, str):
            result = json.loads(result)
        if not result["result"]:
            raise Exception(result["message"])

        data = result["data"]

        # 更新团队令牌使用信息
        group = llm_model.consumer_team or llm_model.team[0]
        used_token = data["input_tokens"] + data["output_tokens"]
        team_info, is_created = TeamTokenUseInfo.objects.get_or_create(
            group=group, llm_model=llm_model.name, defaults={"used_token": used_token}
        )
        if not is_created:
            team_info.used_token += used_token
            team_info.save()

        # 处理内容（可选隐藏思考过程）
        content = data["content"]
        if not show_think:
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        data["content"] = content

        return data, doc_map, title_map

    @staticmethod
    def image_to_base64(image_path: str, log_file: str = "base64.log") -> Optional[str]:
        """
        将图像文件转换为base64字符串并保存到日志文件

        Args:
            image_path: 图像文件路径
            log_file: 保存base64结果的日志文件路径

        Returns:
            图像的base64编码字符串，如果转换失败则返回None
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")

            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                # 保存到日志文件
                with open(log_file, "w") as log:
                    log.write(encoded_string)

                return encoded_string

        except Exception as e:
            logger.error(f"Error converting image to base64: {e}")
            return None

    def search_doc(self, context: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict, Dict]:
        """
        搜索相关文档以提供上下文

        Args:
            context: 当前上下文
            kwargs: 包含搜索所需参数的字典

        Returns:
            更新后的上下文、标题映射和文档映射
        """
        title_map = {}
        score_threshold_map = {i["knowledge_base"]: i["score"] for i in kwargs["rag_score_threshold"]}
        base_ids = list(score_threshold_map.keys())

        # 获取知识库和文档
        knowledge_base_list = KnowledgeBase.objects.filter(id__in=base_ids)
        doc_list = list(
            KnowledgeDocument.objects.filter(knowledge_base_id__in=base_ids).values(
                "id", "knowledge_source_type", "name", "knowledge_base_id"
            )
        )
        doc_map = {i["id"]: i for i in doc_list}

        # 为每个知识库搜索相关文档
        for knowledge_base in knowledge_base_list:
            params = {
                "enable_rerank": knowledge_base.enable_rerank,
                "embed_model": knowledge_base.embed_model.id,
                "rerank_model": knowledge_base.rerank_model_id,
                "rag_k": knowledge_base.rag_k,
                "rag_num_candidates": knowledge_base.rag_num_candidates,
                "enable_text_search": knowledge_base.enable_text_search,
                "text_search_weight": knowledge_base.text_search_weight,
                "enable_vector_search": knowledge_base.enable_vector_search,
                "vector_search_weight": knowledge_base.vector_search_weight,
                "text_search_mode": knowledge_base.text_search_mode,
            }
            score_threshold = score_threshold_map.get(knowledge_base.id, 0.7)

            # 执行搜索
            rag_result = self.knowledge_search_service.search(
                knowledge_base, kwargs["user_message"], params, score_threshold=score_threshold
            )

            # 构建上下文
            context += _(
                """
The following is the background knowledge provided to you. The format of the background knowledge is as follows:
--------
Knowledge Title: [Title]
Knowledge Content: [Content]
--------

             """
            )

            # 添加每个搜索结果到上下文
            for result in rag_result:
                context += "--------\n"
                context += _("Knowledge Title:[{}]\n").format(result["knowledge_title"])
                context += _("Knowledge Content:[{}]\n").format(result["content"].replace("{", "").replace("}", ""))

                # 将结果添加到标题映射
                title_map.setdefault(result["knowledge_id"], []).append(
                    {
                        "content": result["content"],
                        "score": result["score"],
                    }
                )

        return context, title_map, doc_map


# 创建服务实例
llm_service = LLMService()
