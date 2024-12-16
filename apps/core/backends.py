import logging
import traceback

from django.contrib.auth.backends import ModelBackend
from django.core.cache import caches
from django.db import IntegrityError
from django.utils import translation

from apps.core.models import User
from apps.core.utils.keycloak_client import KeyCloakClient

logger = logging.getLogger("app")
cache = caches["db"]


class APISecretAuthBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, api_token=None):
        if not api_token:
            return None
        user_secret = UserAPISecret.objects.filter(api_secret=api_token).first()
        if user_secret:
            user = User.objects.get(username=user_secret.username)
            user.group_list = [user_secret.team]
            return user
        return None


class KeycloakAuthBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, token=None):
        # 判断是否传入验证所需的bk_token,没传入则返回None
        if not token:
            return None
        client = KeyCloakClient()
        is_active, user_info = client.token_is_valid(token)
        # 判断token是否验证通过,不通过则返回None
        if not is_active:
            return None
        if user_info.get("locale"):
            translation.activate(user_info["locale"])
        roles = user_info["realm_access"]["roles"]
        groups = cache.get(f"group_{user_info['sub']}")
        if not groups:
            groups = client.get_user_groups(user_info["sub"], "admin" in roles)
            cache.set(f"group_{user_info['sub']}", groups, 60 * 30)
        return self.set_user_info(groups, roles, user_info)

    @staticmethod
    def set_user_info(groups, roles, user_info):
        try:
            user, _ = User.objects.get_or_create(username=user_info["username"])
            user.email = user_info.get("email", "")
            user.is_superuser = "admin" in roles
            user.is_staff = user.is_superuser
            user.group_list = groups
            user.roles = roles
            user.locale = user_info.get("locale", "zh-Hans")
            user.save()
            return user
        except IntegrityError:
            logger.exception(traceback.format_exc())
            logger.exception("get_or_create UserModel fail or update_or_create UserProperty")
            return None
        except Exception:
            logger.exception(traceback.format_exc())
            logger.exception("Auto create & update UserModel fail")
            return None
