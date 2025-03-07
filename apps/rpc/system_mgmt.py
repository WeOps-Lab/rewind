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

    def search_groups(self, query_params):
        """
        :param query_params: {"page_size": 10, "page": 1, "search": ""}
        """
        return_data = self.client.run("search_groups", query_params=query_params)
        return return_data

    def search_users(self, query_params):
        """
        :param query_params: {"page_size": 10, "page": 1, "search": ""}
        """
        return_data = self.client.run("search_users", query_params=query_params)
        return return_data

    def get_all_groups(self):
        return_data = self.client.run("get_all_groups")
        return return_data

    def search_channel_list(self, channel_type):
        """
        :param channel_type: str， 目前只有email、enterprise_wechat
        """
        return_data = self.client.run("search_channel_list", channel_type=channel_type)
        return return_data

    def send_msg_with_channel(self, channel_id, title, content, receivers):
        """
        :param channel_id: 1 通道id
        :param title: 邮件主题  企微传空字符串即可
        :param content: 正文
        :param receivers: ["abc@canway.net"] 企微传用户的ID列表
        """
        return_data = self.client.run(
            "search_channel_list", channel_id=channel_id, title=title, content=content, receivers=receivers
        )
        return return_data
