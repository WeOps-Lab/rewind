from apps.core.utils.user_group import Group
from apps.core.utils.keycloak_client import KeyCloakClient


class UserGroup:
    def __init__(self):
        self.keycloak_client = KeyCloakClient()

    def user_list(self, query_params):
        """用户列表"""
        users = self.keycloak_client.realm_client.get_users(query_params)
        return {"count": len(users), "users": users}

    def goups_list(self, query_params):
        """用户组列表"""
        if query_params is None:
            query_params = {"search": ""}
        groups = self.keycloak_client.realm_client.get_groups(query_params)
        return groups

    def user_goups_list(self, token):
        """用户组列表"""
        # 查询用户角色
        is_super_admin = self.keycloak_client.is_super_admin(token)
        if is_super_admin:
            return dict(is_all=True, group_ids=[])
        group_ids = Group(token).get_user_group_and_subgroup_ids()
        return dict(is_all=False, group_ids=group_ids)
