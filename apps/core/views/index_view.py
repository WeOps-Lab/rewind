from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from apps.rpc.system_mgmt import SystemMgmt


def index(request):
    data = {"STATIC_URL": "static/", "RUN_MODE": "PROD"}
    response = render(request, "index.prod.html", data)
    return response


@api_view(["GET"])
def login_info(request):
    return JsonResponse(
        {
            "result": True,
            "data": {
                "username": request.user.username,
                "is_superuser": request.user.is_superuser,
                "group_list": request.user.group_list,
                "roles": request.user.roles,
            },
        }
    )


def get_client(request):
    client = SystemMgmt()
    return_data = client.get_client("")
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
