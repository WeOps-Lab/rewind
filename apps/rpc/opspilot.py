from apps.rpc.base import RpcClient


class OpsPilot(object):
    def __init__(self):
        self.client = RpcClient("opspilot")

    def init_user_set(self, username, group_id):
        """
        :param username: 用户名
        :param group_id: 组ID
        """
        return_data = self.client.run("init_user_set", username=username, group_id=group_id)
        return return_data
