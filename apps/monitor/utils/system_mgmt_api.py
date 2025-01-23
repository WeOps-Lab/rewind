import os

import requests

from apps.rpc.system_mgmt import SystemMgmt


class SystemMgmtUtils:

    @staticmethod
    def get_user_all():
        result = SystemMgmt().get_all_users()
        return result["data"]
