import json
import logging

from django.core.management import BaseCommand

from apps.core.utils.keycloak_client import KeyCloakClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "初始化Realm"

    def handle(self, *args, **options):
        keycloak_client = KeyCloakClient()
        with open("support-files/keycloak/realm-lite.json", "r") as fp:
            realm_payload = json.load(fp)
            keycloak_client.admin_client.delete_realm("lite")
            keycloak_client.admin_client.import_realm(realm_payload)
        logger.info("Realm data imported successfully.")

        user_id = keycloak_client.realm_client.create_user({
            "username": "admin",
            "email": "admin@dev.cc",
            "enabled": True,
            "firstName": "admin",
            "lastName": "admin",
            "credentials": [{"value": "password", "type": "password"}]
        }, exist_ok=True)
        logger.info(f"User created successfully with id: {user_id}")

        keycloak_client.realm_client.set_user_password(user_id, "password")
        logger.info("Password set successfully.")

        role_id = keycloak_client.realm_client.get_realm_role("admin")
        keycloak_client.realm_client.assign_realm_roles(user_id, [role_id])
        logger.info("Role assigned successfully.")

        groups = keycloak_client.realm_client.get_groups()
        default_group = next((group for group in groups if group.get('name') == 'Default'), None)
        group_id = default_group.get('id')

        keycloak_client.realm_client.group_user_add(user_id, group_id)
        logger.info("User added to group successfully.")

        clients = keycloak_client.realm_client.get_clients()
        target_client = next((client for client in clients if client.get('clientId') == "lite"), None)

        new_secret = keycloak_client.realm_client.generate_client_secrets(target_client["id"])
        print(f"New secret generated: {new_secret['value']}")
        print(f"export KEYCLOAK_WEB_CLIENT_SECRET={new_secret['value']}")
