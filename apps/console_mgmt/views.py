import json

from django.http import JsonResponse

from apps.rpc.opspilot import OpsPilot  # noqa
from apps.rpc.system_mgmt import SystemMgmt


def get_opspilot_quota(request):
    opspilot = OpsPilot()
    res = opspilot.get_my_quota(request.user.username)
    return JsonResponse(res)


def init_user_set(request):
    kwargs = json.loads(request.body)
    client = SystemMgmt()
    res = client.create_default_group(kwargs["group_name"], kwargs["user_id"], request.user.group_list[0]["id"])
    if not res["result"]:
        return JsonResponse(res)
    res = client.join_default_role(kwargs["user_id"])
    if not res["result"]:
        return JsonResponse(res)
    opspilot_client = OpsPilot()
    res = opspilot_client.init_user_set(res["data"]["group_id"], kwargs["group_name"])
    return JsonResponse(res)
