import os

import requests


class NodeApi:
    def __init__(self, token):
        self.token = token
        self.host = os.getenv("NODE_API_URL")

    def get_nodes(self):
        url = f"{self.host}/api/v1/nodes"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_config(self):
        url = f"{self.host}/api/v1/config"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_config(self):
        url = f"{self.host}/api/v1/config"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        return response.json()

