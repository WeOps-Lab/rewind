from apps.rpc.base import RpcClient


class SystemMgmt(object):
    def __init__(self):
        self.client = RpcClient("system_mgmt")

    def get_client(self, client_id):
        return_data = self.client.run("get_client", client_id)
        return return_data

    def get_client_detail(self, client_id):
        """
        :param client_id: 客户端的ID
        """
        return_data = self.client.run("get_client_detail", client_id)
        return return_data

    def get_user_menus(self, client_id, roles, username, is_superuser):
        """
        :param client_id: 客户端的ID
        :param roles: 查询用户的角色ID列表
        :param username: 查询用户的用户名
        :param is_superuser: 是否超管
        """
        return_data = self.client.run(
            "get_user_menus", client_id=client_id, roles=roles, username=username, is_superuser=is_superuser
        )
        return return_data

    def verify_token(self, token, client_id):
        """
        :param token: 用户登录的token
        :param client_id: 当前APP的ID
        """
        return_data = self.client.run("verify_token", token=token, client_id=client_id)
        return return_data

    def get_group_users(self, group):
        """
        :param group: 当前组的ID
        """
        return_data = self.client.run("get_group_users", group=group)
        return return_data

    def get_all_users(self):
        return_data = self.client.run("get_all_users")
        return return_data

    def get_all_groups(self, params):
        return_data = self.client.run("get_groups")
        return return_data
