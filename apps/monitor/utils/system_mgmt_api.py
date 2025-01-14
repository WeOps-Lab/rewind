import os

import requests

from apps.rpc.system_mgmt import SystemMgmt


class SystemMgmtUtils:

    @staticmethod
    def get_user_all():
        return SystemMgmt().get_all_users()
