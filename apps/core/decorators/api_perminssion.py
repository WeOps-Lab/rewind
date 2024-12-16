import logging
from functools import wraps

from django.utils.translation import gettext as _
from django.views.generic.base import View

from apps.core.utils.web_utils import WebUtils

logger = logging.getLogger("app")


class HasRole(object):
    """
    decorator. log exception if task_definition has
    """

    def __init__(self, roles=None):
        if roles is None:
            roles = []
        if isinstance(roles, str):
            roles = [roles]
        self.roles = roles

    def __call__(self, task_definition):
        @wraps(task_definition)
        def wrapper(*args, **kwargs):
            request = args[0]
            if isinstance(request, View):
                request = args[1]
            if getattr(request, "api_pass", False):
                return task_definition(*args, **kwargs)
            user_info = request.user
            if not self.roles:
                return task_definition(*args, **kwargs)
            roles = user_info.roles
            for i in roles:
                if i in self.roles:
                    return task_definition(*args, **kwargs)
            return WebUtils.response_403(_("insufficient permissions"))

        return wrapper
