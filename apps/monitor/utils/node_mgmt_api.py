import os

import requests


class NodeApi:
    def __init__(self, token):
        self.token = token
        self.host = self.get_url()

    def get_url(self):
        url = os.getenv("NODE_MANAGE_URL")
        if not url:
            raise ValueError("NODE_MANAGE_URL is not set")
        return url

    def get_nodes(self, cloud_region_id, page, page_size, is_superuser, organization_ids: list):
        url = f"{self.host}/node_mgmt/api/node"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"cloud_region_id": cloud_region_id, "page": page, "page_size": page_size}
        if not is_superuser:
            params["organization_ids"] = ",".join(organization_ids)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_collectors(self, name=None, node_operating_system=None):
        url = f"{self.host}/node_mgmt/api/collector"
        params = {}
        if name:
            params["name"] = name
        if node_operating_system:
            params["node_operating_system"] = node_operating_system
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_config_detail(self, config_id):
        url = f"{self.host}/node_mgmt/api/configuration/{config_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_config(self, data: dict):
        url = f"{self.host}/node_mgmt/api/configuration"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_config(self, id: str, data: dict):
        url = f"{self.host}/node_mgmt/api/configuration/{id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def node_asso_config(self, node_id, config_id):
        url = f"{self.host}/node_mgmt/api/configuration/apply_to_node"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"node_id": node_id, "collector_configuration_id": config_id}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
