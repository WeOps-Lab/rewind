import json

import nats_client
from django.http import JsonResponse


async def get_client(request):
    return_data = await nats_client.request("system_mgmt", "get_client")
    return JsonResponse(json.loads(return_data))


async def get_client_detail(request):
    return_data = await nats_client.request(
        "system_mgmt",
        "get_client_detail",
        request.GET["client_id"],
    )

    return JsonResponse(json.loads(return_data))


async def get_user_menus(request):
    return_data = await nats_client.request(
        "system_mgmt",
        "get_user_menus",
        client_id=request.GET["id"],
        roles=request.user.roles,
        username=request.user.username,
    )
    return JsonResponse(json.loads(return_data))
