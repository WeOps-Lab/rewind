from django.utils.translation import gettext_lazy as _

import nats_client
from apps.core.backends import cache
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.system_mgmt.services.group_manage import GroupManage
from apps.system_mgmt.services.role_manage import RoleManage
from apps.system_mgmt.services.user_manage import UserManage


@nats_client.register
def verify_token(token, client_id):
    if not token:
        return {"result": False, "message": _("Token is missing")}
    client = KeyCloakClient()
    is_active, user_info = client.token_is_valid(token)
    if not is_active:
        return {"result": False, "message": _("Token is invalid")}
    roles = user_info["realm_access"]["roles"]
    is_superuser = "admin" in roles or f"{client_id}_admin" in roles
    groups = cache.get(f"group_{user_info.get('username')}")
    if not groups:
        groups = client.get_user_groups(user_info.get("sub"), is_superuser)
        cache.set(f"group_{user_info.get('username')}", groups, 60 * 5)
    return {
        "result": True,
        "data": {
            "username": user_info["username"],
            "email": user_info.get("email", ""),
            "is_superuser": is_superuser,
            "group_list": groups,
            "roles": roles,
            "locale": user_info.get("locale", "en"),
        },
    }


@nats_client.register
def get_user_menus(client_id, roles, username, is_superuser):
    client = RoleManage()
    client_id = client_id
    menus = []
    if not is_superuser:
        policy_ids = client.get_policy_by_by_roles(client_id, roles)
        for i in policy_ids:
            menus.extend(client.role_menus(client_id, i))
        menus = list(set(menus))
    user_menus = client.get_all_menus(client_id, user_menus=menus, username=username, is_superuser=is_superuser)
    return {"result": True, "data": user_menus}


@nats_client.register
def get_client(client_id=""):
    client = KeyCloakClient()
    res = client.realm_client.get_clients()
    if client_id:
        filter_client = [client_id]
    else:
        filter_client = [i["clientId"] for i in res]
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
            if i["clientId"] in filter_client and i.get("authorizationServicesEnabled")
        ],
    }


@nats_client.register
def get_client_detail(client_id):
    client = KeyCloakClient()
    res = client.realm_client.get_client(client_id=client_id)
    return {"result": True, "data": res}


@nats_client.register
def get_group_users(group):
    client = KeyCloakClient()
    users = client.realm_client.get_group_members(group)
    return_data = [
        {"username": i["username"], "first_name": i.get("firstName", ""), "last_name": i.get("lastName", "")}
        for i in users
    ]
    return {"result": True, "data": return_data}


@nats_client.register
def get_all_users():
    client = UserManage()
    res = client.user_all()
    return {"result": True, "data": res}


@nats_client.register
def search_groups(query_params):
    _first, _max = UserManage.get_first_and_max(query_params)
    kwargs = {
        "first": _first,
        "max": _max,
        "search": query_params.get("search", ""),
    }
    client = GroupManage()
    if query_params.get("page"):
        res = client.group_list(kwargs)
    else:
        res = client.group_list(query_params)
    return {"result": True, "data": res}


@nats_client.register
def search_users(query_params):
    _first, _max = UserManage.get_first_and_max(query_params)
    kwargs = {
        "first": _first,
        "max": _max,
        "search": query_params.get("search", ""),
    }
    client = UserManage()
    if query_params.get("page"):
        res = client.user_list(kwargs)
    else:
        res = client.user_list(query_params)
    return {"result": True, "data": res}


@nats_client.register
def get_all_groups():
    client = KeyCloakClient()
    return_data = client.get_user_groups("", True)
    return {"result": True, "data": return_data}
