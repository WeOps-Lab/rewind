from apps.rpc.base import RpcClient


class SystemMgmt(object):
    def __init__(self):
        self.client = RpcClient('system_mgmt')

    def get_client(self):
        return_data = self.client.run('get_client')
        return return_data

    def get_client_detail(self, client_id):
        """
        :param client_id: 客户端的ID
        """
        return_data = self.client.run('get_client_detail', client_id)
        return return_data

    def get_user_menus(self, client_id, roles, username):
        """
        :param client_id: 客户端的ID
        :param roles: 查询用户的角色ID列表
        :param username: 查询用户的用户名
        """
        return_data = self.client.run(
            'get_user_menus',
            client_id=client_id,
            roles=roles,
            username=username
        )
        return return_data

    def verify_token(self, token):
        """
        :param token: 用户登录的token
        """
        return_data = self.client.run(
            'verify_token',
            token=token,
        )
        return return_data
