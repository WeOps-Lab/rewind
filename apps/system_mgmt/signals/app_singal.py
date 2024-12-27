# import json
# import os
#
# from django.conf import settings
#
# from apps.core.utils.keycloak_client import KeyCloakClient
#
#
# def init_apps(**kwargs):
#     client = KeyCloakClient()
#     app_map = get_app_map()
#     for app, menus in app_map:
#         payload = {
#             "clientId": app,
#             "authorizationServicesEnabled": True,
#             "directAccessGrantsEnabled": True,
#         }
#         client_id = client.realm_client.create_client(payload, True)
#
#
# def get_app_map():
#     templates_dir = os.path.join(settings.APPS_DIR, "system_mgmt", "templates")
#     if not os.path.exists(templates_dir):
#         return
#     app_map = {}
#     for i in os.listdir(templates_dir):
#         if i.endswith(".json"):
#             with open(os.path.join(templates_dir, i), "r") as f:
#                 content = f.read()
#                 app_map[i.split(".json")[0]] = json.loads(content)["menus"]
#     return app_map
