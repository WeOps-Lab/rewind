from django.http import JsonResponse
from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.quota_rule_mgmt.quota_utils import get_quota_client
from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.viewset_utils import AuthViewSet
from apps.knowledge_mgmt.models import KnowledgeBase
from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from apps.model_provider_mgmt.models.llm_skill import SkillRequestLog, SkillTools
from apps.model_provider_mgmt.serializers.llm_serializer import (
    LLMModelSerializer,
    LLMSerializer,
    SkillRequestLogSerializer,
    SkillToolsSerializer,
)
from apps.model_provider_mgmt.services.llm_service import llm_service


class LLMFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class LLMViewSet(AuthViewSet):
    serializer_class = LLMSerializer
    queryset = LLMSkill.objects.all()
    filterset_class = LLMFilter

    def _validate_name(self, skill_list, group_list, team):
        exist_teams = []
        for i in skill_list:
            exist_teams.extend(i)
        team_name_map = {i["id"]: i["name"] for i in group_list}
        for i in team:
            if i in exist_teams:
                return _(f"A skill with the same name already exists in group {team_name_map.get(i)}.")
        return ""

    def create(self, request, *args, **kwargs):
        params = request.data
        client = get_quota_client(request)
        skill_count, used_skill_count, __ = client.get_skill_quota()
        if skill_count != -1 and skill_count <= used_skill_count:
            return JsonResponse({"result": False, "message": _("Skill count exceeds quota limit.")})
        skill_list = list(LLMSkill.objects.filter(name=params["name"]).values_list("team", flat=True))
        validate_msg = self._validate_name(skill_list, request.user.group_list, params["team"])
        if validate_msg:
            return JsonResponse({"result": False, "message": validate_msg})
        params["enable_conversation_history"] = True
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance: LLMSkill = self.get_object()
        params = request.data
        skill_list = list(
            LLMSkill.objects.filter(name=params["name"]).exclude(id=instance.id).values_list("team", flat=True)
        )
        validate_msg = self._validate_name(skill_list, request.user.group_list, params["team"])
        if validate_msg:
            return JsonResponse({"result": False, "message": validate_msg})
        if (not request.user.is_superuser) and (instance.created_by != request.user.username):
            params.pop("team", [])
        if "llm_model" in params:
            params["llm_model_id"] = params.pop("llm_model")
        for key in params.keys():
            if hasattr(instance, key):
                setattr(instance, key, params[key])
        instance.updated_by = request.user.username
        if "rag_score_threshold" in params:
            score_threshold_map = {i["knowledge_base"]: i["score"] for i in params["rag_score_threshold"]}
            instance.rag_score_threshold_map = score_threshold_map
            knowledge_base_list = KnowledgeBase.objects.filter(id__in=list(score_threshold_map.keys()))
            instance.knowledge_base.set(knowledge_base_list)
        instance.save()
        return JsonResponse({"result": True})

    @action(methods=["POST"], detail=False)
    @HasRole()
    def execute(self, request):
        """
        {
            "user_message": "你好", # 用户消息
            "llm_model": 1, # 大模型ID
            "skill_prompt": "abc", # Prompt
            "enable_rag": True, # 是否启用RAG
            "enable_rag_knowledge_source": True, # 是否显示RAG知识来源
            "rag_score_threshold": [{"knowledge_base": 1, "score": 0.7}], # RAG分数阈值
            "chat_history": "abc", # 对话历史
            "conversation_window_size": 10, # 对话窗口大小
            "show_think": True # 是否展示think的内容
        }
        """
        params = request.data
        params["username"] = request.user.username
        params["user_id"] = request.user.id
        return_data = llm_service.chat(params)
        return JsonResponse({"result": True, "data": return_data})


class LLMModelViewSet(AuthViewSet):
    serializer_class = LLMModelSerializer
    queryset = LLMModel.objects.all()
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        params = request.data
        if not params.get("team"):
            return JsonResponse({"result": False, "message": _("The team is empty.")})
        LLMModel.objects.create(
            name=params["name"],
            llm_model_type=params["llm_model_type"],
            llm_config=params["llm_config"],
            enabled=params.get("enabled", True),
            team=params.get("team"),
            is_build_in=False,
        )
        return JsonResponse({"result": True})

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_build_in:
            return JsonResponse({"result": False, "message": _("Built-in model is not allowed to be deleted")})
        return super().destroy(request, *args, **kwargs)


class LogFilter(FilterSet):
    skill_id = filters.NumberFilter(field_name="skill_id", lookup_expr="exact")
    current_ip = filters.CharFilter(field_name="current_ip", lookup_expr="icontains")
    start_time = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_time = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")


class SkillRequestLogViewSet(viewsets.ModelViewSet):
    serializer_class = SkillRequestLogSerializer
    queryset = SkillRequestLog.objects.all()
    filterset_class = LogFilter
    ordering = ("-created_at",)

    def list(self, request, *args, **kwargs):
        if not request.GET.get("skill_id"):
            return JsonResponse({"result": False, "message": _("Skill id not found")})
        return super().list(request, *args, **kwargs)


class ToolsFilter(FilterSet):
    display_name = filters.CharFilter(field_name="display_name", lookup_expr="icontains")


class SkillToolsViewSet(AuthViewSet):
    serializer_class = SkillToolsSerializer
    queryset = SkillTools.objects.all()
    filterset_class = ToolsFilter
