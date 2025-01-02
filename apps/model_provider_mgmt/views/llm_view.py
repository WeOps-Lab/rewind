from django.http import JsonResponse
from django.utils.translation import gettext as _
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.quota_rule_mgmt.quota_utils import get_quota_client
from apps.core.decorators.api_perminssion import HasRole
from apps.core.utils.viewset_utils import AuthViewSet
from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBase
from apps.model_provider_mgmt.models import LLMModel, LLMSkill
from apps.model_provider_mgmt.serializers.llm_serializer import LLMModelSerializer, LLMSerializer
from apps.model_provider_mgmt.services.llm_service import llm_service


class ObjFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class LLMViewSet(AuthViewSet):
    serializer_class = LLMSerializer
    queryset = LLMSkill.objects.all()
    filterset_class = ObjFilter

    def create(self, request, *args, **kwargs):
        params = request.data
        client = get_quota_client(request)
        skill_count, used_skill_count, __ = client.get_skill_quota()
        if skill_count != -1 and skill_count <= used_skill_count:
            return JsonResponse({"result": False, "message": _("Skill count exceeds quota limit.")})
        if LLMSkill.objects.filter(name=params["name"]).exists():
            return JsonResponse({"result": False, "message": _("The name already exists.")})
        params["enable_conversation_history"] = True
        serializer = self.get_serializer(data=params)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @HasRole()
    def list(self, request, *args, **kwargs):
        # name = request.GET.get("name", "")
        # queryset = LLMSkill.objects.filter(name__icontains=name)
        queryset = self.filter_queryset(self.get_queryset())
        return self.query_by_groups(request, queryset)

    def update(self, request, *args, **kwargs):
        instance: LLMSkill = self.get_object()
        params = request.data
        if LLMSkill.objects.filter(name=params["name"]).exclude(id=instance.id).exists():
            return JsonResponse({"result": False, "message": "The name already exists."})
        if "llm_model" in params:
            params["llm_model_id"] = params.pop("llm_model")
        for key in params.keys():
            if hasattr(instance, key):
                setattr(instance, key, params[key])
        # instance.name = params["name"]
        # instance.team = params["team"]
        # instance.introduction = params["introduction"]
        # instance.llm_model_id = params.get("llm_model", instance.llm_model_id)
        # instance.skill_prompt = params["skill_prompt"]
        # instance.enable_conversation_history = params["enable_conversation_history"]
        # instance.conversation_window_size = params.get("conversation_window_size", 10)
        # instance.enable_rag = params["enable_rag"]
        # instance.temperature = params["temperature"]
        # instance.enable_rag_knowledge_source = params["enable_rag_knowledge_source"]
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
            "conversation_window_size": 10 # 对话窗口大小
        }
        """
        params = request.data
        params["username"] = request.user.username
        params["user_id"] = request.user.id
        return_data = llm_service.chat(params)
        return JsonResponse({"result": True, "data": return_data})


class LLMModelViewSet(GuardianModelViewSet):
    serializer_class = LLMModelSerializer
    queryset = LLMModel.objects.all()
    search_fields = ["name"]
