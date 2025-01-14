import datetime
import hashlib
import json

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import FileResponse, JsonResponse
from django_minio_backend import MinioBackend

from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.bot_mgmt.models.bot import BotChannel
from apps.bot_mgmt.services.skill_excute_service import SkillExecuteService
from apps.bot_mgmt.utils import set_time_range

# from apps.core.decorators.api_perminssion import HasRole
from apps.core.logger import logger
from apps.core.utils.exempt import api_exempt
from apps.model_provider_mgmt.models import TokenConsumption


@api_exempt
def get_bot_detail(request, bot_id):
    api_token = request.META.get("HTTP_AUTHORIZATION").split("TOKEN")[-1].strip()
    if not api_token:
        return JsonResponse({})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        return JsonResponse({})
    channels = BotChannel.objects.filter(bot_id=bot_id, enabled=True)
    return_data = {
        "channels": [
            {
                "id": i.id,
                "name": i.name,
                "channel_type": i.channel_type,
                "channel_config": i.decrypted_channel_config,
            }
            for i in channels
        ],
    }
    return JsonResponse(return_data)


@api_exempt
def model_download(request):
    bot_id = request.GET.get("bot_id")
    bot = Bot.objects.filter(id=bot_id).first()
    if not bot:
        return JsonResponse({})
    rasa_model = bot.rasa_model
    if not rasa_model:
        return JsonResponse({})
    storage = MinioBackend(bucket_name="munchkin-private")
    file = storage.open(rasa_model.model_file.name, "rb")

    # Calculate ETag
    data = file.read()
    etag = hashlib.md5(data).hexdigest()

    # Reset file pointer to start
    file.seek(0)

    response = FileResponse(file)
    response["ETag"] = etag

    return response


@api_exempt
def skill_execute(request):
    kwargs = json.loads(request.body)
    logger.info(f"skill_execute kwargs: {kwargs}")
    skill_id = kwargs.get("skill_id")
    user_message = kwargs.get("user_message")
    sender_id = kwargs.get("sender_id", "")
    chat_history = kwargs.get("chat_history", [])
    bot_id = kwargs.get("bot_id")
    channel = kwargs.get("channel", "socketio")
    if channel == "socketio":
        channel = "web"
    api_token = request.META.get("HTTP_AUTHORIZATION").split("TOKEN")[-1].strip()
    if not api_token:
        return JsonResponse({"result": {"content": "No authorization"}})
    bot = Bot.objects.filter(id=bot_id, api_token=api_token).first()
    if not bot:
        logger.info(f"api_token: {api_token}")
        return JsonResponse({"result": {"content": "No bot found"}})
    result = SkillExecuteService.execute_skill(bot, skill_id, user_message, chat_history, sender_id, channel)

    return JsonResponse({"result": result})


# @HasRole("admin")
def get_total_token_consumption(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    total_tokens = TokenConsumption.objects.filter(
        created_at__range=[start_time, end_time],
        bot_id=request.GET.get("bot_id"),
    ).aggregate(total_input_tokens=Sum("input_tokens"), total_output_tokens=Sum("output_tokens"))
    input_tokens = total_tokens["total_input_tokens"] or 0
    output_tokens = total_tokens["total_output_tokens"] or 0
    total_combined_tokens = input_tokens + output_tokens
    return JsonResponse({"result": True, "data": total_combined_tokens})


# @HasRole("admin")
def get_token_consumption_overview(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    num_days = (end_time - start_time).days + 1
    all_dates = [start_time + datetime.timedelta(days=i) for i in range(num_days)]
    formatted_dates = {date.strftime("%Y-%m-%d"): 0 for date in all_dates}
    # 查询特定日期范围内的TokenConsumption，并按天分组统计input_tokens和output_tokens的总和
    queryset = (
        TokenConsumption.objects.filter(created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"))
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(input_tokens_sum=Sum("input_tokens"), output_tokens_sum=Sum("output_tokens"))
    )

    # 更新字典与查询结果
    for entry in queryset:
        date = entry["date"].strftime("%Y-%m-%d")
        input_tokens = entry["input_tokens_sum"] or 0
        output_tokens = entry["output_tokens_sum"] or 0
        formatted_dates[date] = input_tokens + output_tokens

    # 转换为所需的输出格式
    result = [{"time": date, "count": values} for date, values in sorted(formatted_dates.items())]
    return JsonResponse({"result": True, "data": result})


# @HasRole("admin")
def get_conversations_line_data(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    queryset = (
        BotConversationHistory.objects.filter(
            created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"), conversation_role="bot"
        )
        .annotate(date=TruncDate("created_at"))
        .values("channel_user__channel_type", "date")
        .annotate(count=Count("id"))  # 不去重，按记录统计
    )
    # 生成日期范围内的所有日期
    result = set_channel_type_line(end_time, queryset, start_time)
    return JsonResponse({"result": True, "data": result})


# @HasRole("admin")
def get_active_users_line_data(request):
    start_time_str = request.GET.get("start_time")
    end_time_str = request.GET.get("end_time")
    end_time, start_time = set_time_range(end_time_str, start_time_str)
    queryset = (
        BotConversationHistory.objects.filter(
            created_at__range=[start_time, end_time], bot_id=request.GET.get("bot_id"), conversation_role="user"
        )
        .annotate(date=TruncDate("created_at"))
        .values("channel_user__channel_type", "date")
        .annotate(count=Count("channel_user", distinct=True))
    )
    # 生成日期范围内的所有日期
    result = set_channel_type_line(end_time, queryset, start_time)
    return JsonResponse({"result": True, "data": result})


def set_channel_type_line(end_time, queryset, start_time):
    num_days = (end_time - start_time).days + 1
    all_dates = [start_time + datetime.timedelta(days=i) for i in range(num_days)]
    formatted_dates = {date.strftime("%Y-%m-%d"): 0 for date in all_dates}
    known_channel_types = ["web", "ding_talk", "enterprise_wechat"]
    result_dict = {channel_type: formatted_dates.copy() for channel_type in known_channel_types}
    total_user_count = formatted_dates.copy()
    # 更新字典与查询结果
    for entry in queryset:
        channel_type = entry["channel_user__channel_type"]
        date = entry["date"].strftime("%Y-%m-%d")
        user_count = entry["count"]
        result_dict[channel_type][date] = user_count
        total_user_count[date] += user_count
    # 转换为所需的输出格式
    result = {
        channel_type: [{"time": date, "count": user_count} for date, user_count in sorted(date_dict.items())]
        for channel_type, date_dict in result_dict.items()
    }
    result["total"] = [{"time": date, "count": user_count} for date, user_count in sorted(total_user_count.items())]
    return result
