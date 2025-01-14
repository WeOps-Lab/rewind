from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class ActionChoice(object):
    USE_KNOWLEDGE = 0

    CHOICE = ((USE_KNOWLEDGE, _("Use specified knowledge base")),)


class LLMSkill(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="名称")
    llm_model = models.ForeignKey(
        "model_provider_mgmt.LLMModel", on_delete=models.CASCADE, verbose_name="LLM模型", blank=True, null=True
    )
    skill_id = models.CharField(max_length=255, verbose_name="技能ID", blank=True, null=True)
    skill_prompt = models.TextField(blank=True, null=True, verbose_name="技能提示词")

    enable_conversation_history = models.BooleanField(default=False, verbose_name="启用对话历史")
    conversation_window_size = models.IntegerField(default=10, verbose_name="对话窗口大小")

    enable_rag = models.BooleanField(default=False, verbose_name="启用RAG")
    enable_rag_knowledge_source = models.BooleanField(default=False, verbose_name="显示RAG知识来源")
    rag_score_threshold_map = models.JSONField(default=dict, verbose_name="知识库RAG分数阈值映射")
    knowledge_base = models.ManyToManyField("knowledge_mgmt.KnowledgeBase", blank=True, verbose_name="知识库")
    introduction = models.TextField(blank=True, null=True, default="", verbose_name="介绍")
    team = models.JSONField(default=list, verbose_name="分组")

    temperature = models.FloatField(default=0.7, verbose_name="温度")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLM技能管理"
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(fields=["created_by", "name"], name="unique_owner_name")]


class SkillRule(MaintainerInfo, TimeInfo):
    skill = models.ForeignKey("model_provider_mgmt.LLMSkill", on_delete=models.CASCADE, verbose_name="技能")
    name = models.CharField(max_length=255, verbose_name="规则名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    condition = models.JSONField(default=dict, verbose_name="条件")
    action = models.IntegerField(default=0, verbose_name="动作", choices=ActionChoice.CHOICE)
    action_set = models.JSONField(default=dict, verbose_name="动作设置")
    is_enabled = models.BooleanField(default=True, verbose_name="是否启用")
