import nats_client
from apps.base.models import QuotaRule
from apps.core.logger import logger
from apps.model_provider_mgmt.models import LLMModel


@nats_client.register
def init_user_set(group_id, group_name):
    try:
        llm_model_list = LLMModel.objects.filter(is_build_in=True)
        add_model_list = []
        name_list = set()
        for llm_model in llm_model_list:
            llm_model.id = None
            llm_model.team = [group_id]
            llm_model.consumer_team = group_id
            llm_model.is_build_in = False
            decrypted_llm_config = llm_model.decrypted_llm_config
            llm_model.llm_config = decrypted_llm_config
            add_model_list.append(llm_model)
            name_list.add(llm_model.name)
        LLMModel.objects.bulk_create(add_model_list)
        QuotaRule.objects.create(
            name=f"group-{group_name}-llm-quota",
            target_type="group",
            target_list=[group_id],
            rule_type="shared",
            file_size=50,
            unit="MB",
            skill_count=2,
            bot_count=2,
            token_set={key: {"value": 10, "unit": "thousand"} for key in name_list},
        )
        return {"result": True}
    except Exception as e:
        logger.exception(e)
        return {"result": False, "message": str(e)}
