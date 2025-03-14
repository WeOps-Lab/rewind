import json

from django.http import JsonResponse

from apps.rpc.opspilot import OpsPilot  # noqa
from apps.rpc.system_mgmt import SystemMgmt


def get_opspilot_quota(request):
    return JsonResponse({"result": True, "data": []})


def init_user_set(request):
    kwargs = json.loads(request.body)
    client = SystemMgmt()
    res = client.create_default_group(kwargs["group_name"], kwargs["user_id"])
    if not res["result"]:
        return JsonResponse(res)
    opspilot_client = OpsPilot()
    res = opspilot_client.init_user_set(request.user.username, res["data"]["group_id"])
    return JsonResponse(res)
