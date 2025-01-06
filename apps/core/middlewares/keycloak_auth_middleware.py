import logging

from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _
from rest_framework.permissions import AllowAny

from apps.core.utils.web_utils import WebUtils


class KeyCloakAuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.logger = logging.getLogger(__name__)

    def process_view(self, request, view, args, kwargs):
        if any([
            getattr(view, "api_exempt", False),
            getattr(request, "api_pass", False),
            request.path == "/swagger/",
            request.path.startswith("/admin/")
        ]):
            return None

        # 检查是否豁免登录
        if getattr(view, "login_exempt", False):
            return None

        token = request.META.get(settings.AUTH_TOKEN_HEADER_NAME)
        if not token:
            return WebUtils.response_401(_("please provide Token"))

        token = token.split("Bearer ")[-1]
        user = auth.authenticate(request=request, token=token)
        if user:
            auth.login(request, user)
            if not request.session.session_key:
                request.session.cycle_key()
            return None

        return WebUtils.response_401(_("please provide Token"))
