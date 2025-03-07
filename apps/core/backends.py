import logging
import os
import traceback

from django.contrib.auth.backends import ModelBackend
from django.core.cache import caches
from django.db import IntegrityError
from django.utils import translation

from apps.base.models import User, UserAPISecret
from apps.rpc.system_mgmt import SystemMgmt

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
        client = SystemMgmt()
        result = client.verify_token(token, os.getenv("CLIENT_ID", ""))
        # 判断token是否验证通过,不通过则返回None
        if not result["result"]:
            return None
        user_info = result["data"]
        if user_info.get("locale"):
            translation.activate(user_info["locale"])
        return self.set_user_info(user_info)

    @staticmethod
    def set_user_info(user_info):
        try:
            user, _ = User.objects.get_or_create(username=user_info["username"])
            user.email = user_info.get("email", "")
            user.is_superuser = user_info["is_superuser"]
            user.is_staff = user.is_superuser
            user.group_list = user_info["group_list"]
            user.roles = user_info["roles"]
            user.locale = user_info.get("locale", "en")
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
