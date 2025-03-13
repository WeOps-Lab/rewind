from apps.rpc.base import RpcClient


class NodeMgmt(object):
    def __init__(self):
        self.client = RpcClient('node_mgmt')

    def node_list(self, query_data):
        """
        :param query_data: 查询条件
        {
            "cloud_region_id": 1,
            "organization_ids": ["1", "2"],
            "name": "node_name",
            "ip": "10.10.10.1",
            "os": "linux/windows",
            "page": 1,
            "page_size": 10,
        }
        """
        return_data = self.client.run('node_list', query_data)
        return return_data

    def batch_setting_node_child_config(self, data):
        """
        :param data: 批量设置节点子配置
        {
            "object_type": "web",
            "nodes": [{
            "id": "27439797-fd14-4e18-b54e-3f7ce8727030",
            "configs": [{
                    "url": "https://wepaas.canway.net/",
                    "type": "http_response",
                    "instance_id": "https://wepaas.canway.net/"
                    "instance_type": "website"
                    "interval": 10
                }]
            }]
        }
        """
        return_data = self.client.run('batch_setting_node_child_config', data)
        return return_data

    def get_instance_child_config(self, query_data):
        """
        :param query_data: 查询条件
        {
            "collect_type": "http_response", // 非必填
            "config_type": "http_response",  // 非必填
            "collect_instance_id": "https://wepaas.canway.net/"
        }
        """
        return_data = self.client.run('get_instance_child_config', query_data)
        return return_data

    def update_instance_child_config(self, data):
        """
        :param data: 更新实例子配置
        {
            "id": 1,
            "content": ""
        }
        """
        return_data = self.client.run('update_instance_child_config', data)
        return return_data

    def delete_instance_child_config(self, instance_ids):
        """
        :param instance_ids: 实例ID列表
        """
        return_data = self.client.run('delete_instance_child_config', instance_ids)
        return return_data
