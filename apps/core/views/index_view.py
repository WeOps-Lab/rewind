from django.conf import settings
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
    token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME).split("Bearer ")[-1]
    if token is None:
        return WebUtils.response_error(
            error_message=_("please provide Token"),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    client = KeyCloakClient()
    is_active, user_info = client.token_is_valid(token)
    if not is_active:
        return WebUtils.response_error(
            error_message=_("token validation failed"),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if user_info.get("locale"):
        translation.activate(user_info["locale"])
    return WebUtils.response_success({"result": True})
