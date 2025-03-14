from apps.rpc.base import RpcClient


class OpsPilot(object):
    def __init__(self):
        self.client = RpcClient("opspilot")

    def init_user_set(self, group_id, group_name):
        """
        :param group_id: 组ID
        :param group_name: 组名
        """
        return_data = self.client.run("init_user_set", group_id=group_id, group_name=group_name)
        return return_data
