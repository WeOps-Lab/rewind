from rest_framework.authtoken.models import Token

from apps.base.models import User
from apps.model_provider_mgmt.models import (
    EmbedModelChoices,
    EmbedProvider,
    LLMModel,
    LLMModelChoices,
    RerankModelChoices,
    RerankProvider,
)
from apps.model_provider_mgmt.models.llm_skill import SkillTools
from apps.model_provider_mgmt.models.ocr_provider import OCRProvider


class ModelProviderInitService:
    def __init__(self, owner: User):
        self.owner = owner

    def init(self):
        if self.owner.username == "admin":
            RerankProvider.objects.get_or_create(
                name="bce-reranker-base_v1",
                rerank_model_type=RerankModelChoices.LANG_SERVE,
                defaults={"rerank_config": {"base_url": "http://bce-embed-server/rerank"}},
            )

            EmbedProvider.objects.get_or_create(
                name="bce-embedding-base_v1",
                embed_model_type=EmbedModelChoices.LANG_SERVE,
                defaults={
                    "embed_config": {
                        "base_url": "http://bce-embed-server/embed",
                    }
                },
            )

            EmbedProvider.objects.get_or_create(
                name="FastEmbed(BAAI/bge-small-zh-v1.5)",
                embed_model_type=EmbedModelChoices.LANG_SERVE,
                defaults=dict(
                    embed_config={
                        "base_url": "http://fast-embed-server",
                    }
                ),
            )

            LLMModel.objects.get_or_create(
                name="GPT-4 32K",
                llm_model_type=LLMModelChoices.CHAT_GPT,
                is_build_in=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.openai.com",
                        "temperature": 0.7,
                        "model": "gpt-4-32k",
                    }
                },
            )

            LLMModel.objects.get_or_create(
                name="GPT-3.5 Turbo 16K",
                llm_model_type=LLMModelChoices.CHAT_GPT,
                is_build_in=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.openai.com",
                        "temperature": 0.7,
                        "model": "gpt-3.5-turbo-16k",
                    }
                },
            )

            LLMModel.objects.get_or_create(
                name="GPT-4o",
                llm_model_type=LLMModelChoices.CHAT_GPT,
                is_build_in=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.openai.com",
                        "temperature": 0.7,
                        "model": "gpt-4o",
                    }
                },
            )

            LLMModel.objects.get_or_create(
                name="DeepSeek-R1:1.5b",
                llm_model_type=LLMModelChoices.DEEP_SEEK,
                is_build_in=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.deepseek.com",
                        "temperature": 0.7,
                        "model": "deepseek-r1:1.5b",
                    }
                },
            )
            LLMModel.objects.get_or_create(
                name="QwQ",
                llm_model_type=LLMModelChoices.HUGGING_FACE,
                is_build_in=True,
                defaults={
                    "llm_config": {
                        "openai_api_key": "your_openai_api_key",
                        "openai_base_url": "https://api.deepseek.com",
                        "temperature": 0.7,
                        "model": "Qwen/QwQ-32B",
                    }
                },
            )

        Token.objects.get_or_create(user=self.owner)

        OCRProvider.objects.get_or_create(
            name="PaddleOCR",
            defaults={
                "enabled": True,
                "ocr_config": {
                    "base_url": "http://ocr-server/paddle_ocr",
                },
            },
        )

        OCRProvider.objects.get_or_create(
            name="AzureOCR",
            defaults={
                "enabled": True,
                "ocr_config": {
                    "base_url": "http://ocr-server/azure_ocr",
                },
            },
        )
        SkillTools.objects.update_or_create(
            name="Online Search",
            defaults={
                "params": {"url": "http://127.0.0.1:8003/sse", "name": "Online Search"},
                "description": "",
                "tags": ["search"],
                "icon": "",
                "is_build_in": True,
            },
        )
        SkillTools.objects.update_or_create(
            name="General tools",
            defaults={
                "params": {"url": "http://127.0.0.1:8002/sse", "name": "General tools"},
                "description": "",
                "tags": ["general"],
                "icon": "",
                "is_build_in": True,
            },
        )
