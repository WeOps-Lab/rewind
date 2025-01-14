from apps.core.utils.keycloak_client import KeyCloakClient
from apps.system_mgmt.templates.init_menus import MENUS


def init_apps(**kwargs):
    client = KeyCloakClient()
    for app_obj in MENUS:
        payload = {
            "clientId": app_obj["client_id"],
            "name": app_obj["name"],
            "description": app_obj["description"],
            "baseUrl": app_obj["url"],
            "serviceAccountsEnabled": True,
            "directAccessGrantsEnabled": True,
            "authorizationServicesEnabled": True,
        }
        client_id = client.realm_client.create_client(payload, True)
        resource = client.realm_client.get_client_authz_resources(client_id)
        default_resource = [i for i in resource if i["name"] == "Default Resource"]
        if default_resource:
            client.realm_client.delete_client_authz_resource(client_id, default_resource[0]["_id"])
        create_resource(client_id, app_obj["menus"], client)
        create_default_roles(client_id, client, app_obj["roles"])


def create_resource(client_id, menus, client):
    index = 1
    for i in menus:
        for child in i["children"]:
            for operate in child["operation"]:
                payload = {
                    "type": i["name"],
                    "name": f"{child['id']}-{operate}",
                    "displayName": f"{child['name']}-{operate}",
                    "attributes": {"index": index, "url": child["url"], "icon": child["icon"], "title": child["title"]},
                }
                index += 1
                client.realm_client.create_client_authz_resource(client_id, payload, True)


def create_default_roles(client_id, client, roles):
    all_resource = client.realm_client.get_client_authz_resources(client_id)
    for i in roles:
        client.realm_client.create_realm_role({"name": i["role_name"]}, True)
        role_info = client.realm_client.get_realm_role(role_name=i["role_name"])
        policy_data = {
            "type": "role",
            "logic": "POSITIVE",
            "decisionStrategy": "AFFIRMATIVE",
            "name": i["name"],
            "roles": [{"id": role_info["id"]}],
        }
        policy_obj = client.realm_client.create_client_authz_role_based_policy(client_id, policy_data, True)
        if not i["menus"]:
            continue
        menu_ids = [u["_id"] for u in all_resource if u["name"] in i["menus"]]
        client.create_permission(client_id, menu_ids, i["name"], policy_obj["id"])


def get_all_clients(client):
    res = client.realm_client.get_clients()
    return_data = {i["clientId"]: {"id": i["id"], "name": i["name"]} for i in res}
    return return_data
