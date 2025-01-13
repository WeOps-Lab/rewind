import json
from functools import wraps

import nats_client
from django.utils.translation import gettext_lazy as _

from apps.core.backends import cache
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.system_mgmt.services.role_manage import RoleManage


def json_dumps_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 调用被装饰的函数
        result = func(*args, **kwargs)
        return json.dumps(result)

    return wrapper


@nats_client.register
@json_dumps_decorator
def verify_token(token):
    if not token:
        return {"result": False, "message": _("Token is missing")}
    client = KeyCloakClient()
    is_active, user_info = client.token_is_valid(token)
    if not is_active:
        return {"result": False, "message": _("Token is invalid")}
    roles = user_info["realm_access"]["roles"]
    groups = cache.get(f"group_{user_info['sub']}")
    if not groups:
        groups = client.get_user_groups(user_info["sub"], "admin" in roles)
        cache.set(f"group_{user_info['sub']}", groups, 60 * 30)
    return {
        "result": True,
        "data": {
            "username": user_info["username"],
            "email": user_info["email"],
            "is_superuser": "admin" in roles,
            "group_list": groups,
            "roles": roles,
            "locale": user_info.get("locale", "en"),
        },
    }


@nats_client.register
@json_dumps_decorator
def get_user_menus(client_id, roles, username):
    client = RoleManage()
    client_id = client_id
    policy_ids = client.get_policy_by_by_roles(client_id, roles)
    menus = []
    for i in policy_ids:
        menus.extend(client.role_menus(client_id, i))
    menus = list(set(menus))
    user_menus = client.get_all_menus(client_id, user_menus=menus, username=username)
    return {"result": True, "data": user_menus}


@nats_client.register
@json_dumps_decorator
def get_client():
    client = KeyCloakClient()
    res = client.realm_client.get_clients()
    return {
        "result": True,
        "data": [
            {
                "id": i["id"],
                "name": i["name"],
                "client_id": i["clientId"],
                "description": i["description"],
                "url": i["baseUrl"],
            }
            for i in res
            if i["clientId"] in ["munchkin", "system_mgmt"]
        ],
    }


@nats_client.register
@json_dumps_decorator
def get_client_detail(client_id):
    client = KeyCloakClient()
    res = client.realm_client.get_client(client_id=client_id)
    return {"result": True, "data": res}
