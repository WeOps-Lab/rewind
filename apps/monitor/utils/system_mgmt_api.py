import os

import requests


class SystemMgmtApi:
    def __init__(self, token):
        self.token = token
        self.host = self.get_url()

    def get_url(self):
        url = os.getenv("SYSTEM_MANAGE_URL")
        if not url:
            raise ValueError("SYSTEM_MANAGE_URL is not set")
        return url

    def get_user_all(self):
        url = f"{self.host}/system_mgmt/user/user_all/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_roles_by_client(self):
        url = f"{self.host}/system_mgmt/role/search_role_list/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params={"client_id": os.getenv("KEYCLOAK_CLIENT_ID")})
        response.raise_for_status()
        return response.json()
