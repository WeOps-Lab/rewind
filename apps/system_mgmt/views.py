from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.keycloak_client import KeyCloakClient
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


def verify_token(request):
    user = request.user
    if not user:
        return JsonResponse({"result": False, "message": _("Token verification failed")})
    return JsonResponse(
        {
            "result": True,
            "data": {
                "username": user.username,
                "email": user.email,
                "is_superuser": user.is_superuser,
                "group_list": user.group_list,
                "roles": user.roles,
                "locale": user.locale,
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
