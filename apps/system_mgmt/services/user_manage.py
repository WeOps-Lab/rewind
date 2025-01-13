import json

from apps.core.utils.keycloak_client import KeyCloakClient


class UserManage(object):
    def __init__(self):
        self.keycloak_client = KeyCloakClient()

    @staticmethod
    def get_first_and_max(params):
        """格式化page参数, 获取first与max"""
        page, page_size = int(params.get("page", 1)), int(params.get("page_size", 20))
        _first = (page - 1) * page_size
        _max = page_size
        return _first, _max

    def group_retrieve(self, group_id):
        """查询某个组织的信息"""
        group = self.keycloak_client.realm_client.get_group(group_id)
        return group

    def user_list(self, query_params, group_id=None):
        """用户列表"""
        if group_id:
            users = self.keycloak_client.realm_client.get_group_members(group_id, query_params)
            user_count = self.keycloak_client.get_group_user_count(group_id, {"search": query_params["search"]})
        else:
            users = self.keycloak_client.realm_client.get_users(query_params)
            user_count = self.keycloak_client.realm_client.users_count(query_params)
        return {"count": user_count, "users": users}

    def user_all(self):
        """获取所有用户"""
        users = self.keycloak_client.realm_client.get_users()
        return users

    def get_user_info(self, user_id, client_id):
        """获取用户信息"""
        user_info = self.keycloak_client.realm_client.get_user(user_id)
        roles = self.get_user_roles(client_id, user_id)
        try:
            groups = self.keycloak_client.realm_client.get_user_groups(user_id)
        except Exception:
            groups = []
            # 用户补充用户组信息
        user_info.update(roles=roles)
        user_info.update(groups=groups)
        return user_info

    def get_user_roles(self, client_id, user_id):
        roles = []
        user_roles = self.keycloak_client.get_realm_roles_of_user(user_id)
        policies = self.keycloak_client.realm_client.get_client_authz_policies(client_id)
        role_map = {i["id"]: i["name"] for i in user_roles}
        for i in policies:
            role_obj = json.loads(i["config"].get("roles", "[]"))
            if not role_obj:
                continue
            role_obj = role_obj[0]
            if role_obj["id"] in role_map:
                roles.append(
                    {
                        "policy_id": i["id"],
                        "display_name": i["name"],
                        "role_id": role_obj["id"],
                        "role_name": role_map.get(role_obj["id"], ""),
                    }
                )
        return roles

    def user_list_by_role(self, role_name):
        """获取角色下用户"""
        result = self.keycloak_client.realm_client.get_realm_role_members(role_name)
        return result

    def user_create(self, data):
        """创建用户"""
        user_info = dict(
            username=data["username"],
            email=data.get("email"),
            lastName=data.get("lastName"),
            enabled=True,
        )
        user_id = self.keycloak_client.realm_client.create_user(user_info)
        self.keycloak_client.realm_client.assign_realm_roles(user_id, data["roles"])
        for group_id in data["groups"]:
            self.keycloak_client.realm_client.group_user_add(user_id, group_id)
        user_info = self.keycloak_client.realm_client.get_user(user_id)
        return user_info

    def user_delete(self, user_ids):
        """删除用户"""
        for user_id in user_ids:
            self.keycloak_client.realm_client.delete_user(user_id)

    def user_update(self, data, user_id):
        """更新用户"""
        roles = data.pop("roles", [])
        groups = data.pop("groups", [])
        old_groups = self.keycloak_client.realm_client.get_user_groups(user_id)
        old_roles = self.keycloak_client.get_realm_roles_of_user(user_id)
        for i in old_groups:
            self.keycloak_client.realm_client.group_user_remove(user_id, i["id"])
        delete_roles = []
        for i in old_roles:
            i.pop("role_type", "")
        self.keycloak_client.realm_client.delete_realm_roles_of_user(user_id, delete_roles)
        self.keycloak_client.realm_client.update_user(user_id, data)
        self.keycloak_client.realm_client.assign_realm_roles(user_id, roles)
        for group_id in groups:
            self.keycloak_client.realm_client.group_user_add(user_id, group_id)

    def user_reset_password(self, data, user_id):
        """重置用户密码"""
        self.keycloak_client.realm_client.set_user_password(user_id, data["password"], False)

    def user_add_groups(self, data, user_id):
        """为用户添加一些组"""
        for group_id in data:
            self.keycloak_client.realm_client.group_user_add(user_id, group_id)

    def user_remove_groups(self, data, user_id):
        """将用户从一些组中移除"""
        for group_id in data:
            self.keycloak_client.realm_client.group_user_remove(user_id, group_id)
