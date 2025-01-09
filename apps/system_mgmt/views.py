from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from apps.core.backends import cache
from apps.core.utils.keycloak_client import KeyCloakClient
from apps.core.utils.open_base import login_exempt
from apps.system_mgmt.services.role_manage import RoleManage


@csrf_exempt
def get_client(request):
    client = KeyCloakClient()
    res = client.realm_client.get_clients()
    return JsonResponse(
        {
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
    )


@csrf_exempt
def get_client_detail(request):
    client = KeyCloakClient()
    res = client.realm_client.get_client(client_id=request.GET["client_id"])
    return JsonResponse({"result": True, "data": res})


@login_exempt
def verify_token(request):
    token = request.GET.get("token")
    if not token:
        return JsonResponse({"result": False, "message": _("Token is missing")})
    client = KeyCloakClient()
    is_active, user_info = client.token_is_valid(token)
    if not is_active:
        return JsonResponse({"result": False, "message": _("Token is invalid")})
    roles = user_info["realm_access"]["roles"]
    groups = cache.get(f"group_{user_info['sub']}")
    if not groups:
        groups = client.get_user_groups(user_info["sub"], "admin" in roles)
        cache.set(f"group_{user_info['sub']}", groups, 60 * 30)
    return JsonResponse(
        {
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
    )


def get_user_menus(request):
    client = RoleManage()
    client_id = request.GET["id"]
    policy_ids = client.get_policy_by_by_roles(client_id, request.user.roles)
    menus = []
    for i in policy_ids:
        menus.extend(client.role_menus(client_id, i))
    menus = list(set(menus))
    user_menus = client.get_all_menus(client_id, user_menus=menus)
    return JsonResponse({"result": True, "data": user_menus})
