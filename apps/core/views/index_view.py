from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework import status

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.web_utils import WebUtils


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

