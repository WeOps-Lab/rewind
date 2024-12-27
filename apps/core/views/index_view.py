from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    data = {"STATIC_URL": "static/", "RUN_MODE": "PROD"}
    response = render(request, "index.prod.html", data)
    return response


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
