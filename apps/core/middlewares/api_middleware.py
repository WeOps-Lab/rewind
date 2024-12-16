from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _
from rest_framework import status

from apps.core.utils.web_utils import WebUtils


class APISecretFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get(settings.API_TOKEN_HEADER_NAME)
        if token is None:
            setattr(request, "api_pass", False)
            return None
        user = auth.authenticate(request=request, api_token=token)
        if user is not None:
            setattr(request, "api_pass", True)
            auth.login(request, user)
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            return None
        return WebUtils.response_error(
            error_message=_("token validation failed"), status_code=status.HTTP_403_FORBIDDEN
        )
