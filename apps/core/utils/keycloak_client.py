import logging

from keycloak import KeycloakAdmin, KeycloakOpenID
from singleton_decorator import singleton

from apps.core.entities.user_token_entity import UserTokenEntity
from config.default import (
    KEYCLOAK_ADMIN_PASSWORD,
    KEYCLOAK_ADMIN_USERNAME,
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_REALM,
    KEYCLOAK_URL_API,
)


@singleton
class KeyCloakClient:
    def __init__(self):
        self.admin_client = KeycloakAdmin(
            server_url=KEYCLOAK_URL_API,
            username=KEYCLOAK_ADMIN_USERNAME,
            password=KEYCLOAK_ADMIN_PASSWORD,
        )
        self.realm_client = KeycloakAdmin(
            server_url=KEYCLOAK_URL_API,
            username=KEYCLOAK_ADMIN_USERNAME,
            password=KEYCLOAK_ADMIN_PASSWORD,
            realm_name=KEYCLOAK_REALM,
            client_id="admin-cli",
            user_realm_name="master",
        )
        self.client_secret_key, self.client_id = None, None
        self.openid_client = None
        self.logger = logging.getLogger("app")

    def get_openid_client(self):
        if self.openid_client is None:
            self.openid_client = KeycloakOpenID(
                server_url=KEYCLOAK_URL_API,
                client_id=KEYCLOAK_CLIENT_ID,
                realm_name=KEYCLOAK_REALM,
                client_secret_key=self.get_client_secret_key(),
            )
        return self.openid_client

    def set_client_secret_and_id(self):
        """设置域id与secret"""
        client_secret_key, client_id = None, None
        clients = self.realm_client.get_clients()
        for client in clients:
            if client["clientId"] == KEYCLOAK_CLIENT_ID:
                client_id = client["id"]
                client_secret_key = client["secret"]
                break
        self.client_secret_key, self.client_id = client_secret_key, client_id

    def get_client_secret_key(self):
        """获取客户端secret_key"""
        if self.client_secret_key is None:
            self.set_client_secret_and_id()
        return self.client_secret_key

    def get_client_id(self):
        """获取客户端client_id"""
        if self.client_id is None:
            self.set_client_secret_and_id()
        return self.client_id

    def get_realm_client(self):
        return self.realm_client

    def token_is_valid(self, token) -> (bool, dict):
        try:
            openid_client = self.get_openid_client()
            token_info = openid_client.introspect(token)
            if token_info.get("active"):
                return True, token_info
            else:
                return False, {}
        except Exception:
            return False, {}

    def get_userinfo(self, token: str):
        openid_client = self.get_openid_client()
        return openid_client.userinfo(token)

    def get_roles(self, token: str) -> list:
        try:
            openid_client = self.get_openid_client()
            token_info = openid_client.introspect(token)
            return token_info["realm_access"]["roles"]
        except Exception:
            self.logger.error("获取用户角色失败")
            return []

    def is_super_admin(self, token: str) -> bool:
        try:
            openid_client = self.get_openid_client()
            token_info = openid_client.introspect(token)
            return "admin" in token_info["realm_access"]["roles"]
        except:  # noqa
            return False

    def has_permission(self, token: str, permission: str) -> bool:
        try:
            openid_client = self.get_openid_client()
            openid_client.uma_permissions(token, permission)
            return True
        except:  # noqa
            return False

    def get_token(self, username: str, password: str) -> UserTokenEntity:
        try:
            openid_client = self.get_openid_client()
            token = openid_client.token(username, password)
            return UserTokenEntity(token=token["access_token"], error_message="", success=True)
        except Exception as e:
            self.logger.error(e)
            return UserTokenEntity(token=None, error_message="用户名密码不匹配", success=False)

    def get_user_groups(self, sub, is_admin):
        all_groups = self.realm_client.get_groups({"search": ""})
        if is_admin:
            return self.get_child_groups(all_groups)
        res = self.realm_client.get_user_groups(sub, {"search": ""})
        return self.get_normal_user_all_groups(res, all_groups)

    def get_normal_user_all_groups(self, res, all_groups):
        exist_data = [i["id"] for i in res]
        return_data = [{"id": i["id"], "name": i["name"], "path": i["path"]} for i in res]
        group_ids = [i["id"] for i in return_data]
        for i in all_groups:
            if i["id"] not in group_ids:
                continue
            sub_groups = i.pop("subGroups", [])
            group_children = [u for u in self.get_child_groups(sub_groups) if u["id"] not in exist_data]
            return_data.extend(group_children)
            exist_data.extend([u["id"] for u in group_children])
        return return_data

    def get_child_groups(self, groups):
        return_data = []
        exist_data = []
        for i in groups:
            sub_groups = i.pop("subGroups", [])
            if i["id"] not in return_data:
                return_data.append({"id": i["id"], "name": i["name"], "path": i["path"]})
                exist_data.append(i["id"])
            if sub_groups:
                group_children = [u for u in self.get_child_groups(sub_groups) if u["id"] not in exist_data]
                return_data.extend(group_children)
                exist_data.extend([u["id"] for u in group_children])
        return return_data
