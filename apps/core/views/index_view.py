import os

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view

from apps.rpc.system_mgmt import SystemMgmt


def index(request):
    data = {"STATIC_URL": "static/", "RUN_MODE": "PROD"}
    response = render(request, "index.prod.html", data)
    return response


@api_view(["GET"])
def login_info(request):
    is_first_login = False
    if not request.user.group_list:
        is_first_login = True
    elif len(request.user.group_list) == 1 and request.user.group_list[0].group_name == os.environ.get(
        "DEFAULT_GROUP_NAME", "Default"
    ):
        is_first_login = True
    client = SystemMgmt()
    res = client.search_users({"search": request.user.username})
    user_id = [i for i in res["data"]["users"] if i["username"] == request.user.username][0]["id"]
    return JsonResponse(
        {
            "result": True,
            "data": {
                "user_id": user_id,
                "username": request.user.username,
                "is_superuser": request.user.is_superuser,
                "group_list": request.user.group_list,
                "roles": request.user.roles,
                "is_first_login": is_first_login,
            },
        }
    )


def get_client(request):
    client = SystemMgmt()
    return_data = client.get_client("")
    return JsonResponse(return_data)


def get_my_client(request):
    client = SystemMgmt()
    client_id = os.getenv("CLIENT_ID", "")
    return_data = client.get_client(client_id)
    return JsonResponse(return_data)


def get_client_detail(request):
    client = SystemMgmt()
    return_data = client.get_client_detail(
        client_id=request.GET["id"],
    )
    return JsonResponse(return_data)


def get_user_menus(request):
    client = SystemMgmt()
    return_data = client.get_user_menus(
        client_id=request.GET["id"],
        roles=request.user.roles,
        username=request.user.username,
        is_superuser=request.user.is_superuser,
    )
    return JsonResponse(return_data)


def get_all_groups(request):
    if not request.user.is_superuser:
        return JsonResponse({"result": False, "message": _("Not Authorized")})
    client = SystemMgmt()
    return_data = client.get_all_groups()
    return JsonResponse(return_data)
