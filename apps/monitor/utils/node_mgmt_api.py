from apps.rpc.node_mgmt import NodeMgmt


class NodeUtils:

    @staticmethod
    def get_nodes(query_data: dict):
        return NodeMgmt().node_list(query_data)

    @staticmethod
    def batch_setting_node_child_config(data: dict):
        return NodeMgmt().batch_setting_node_child_config(data)

    @staticmethod
    def get_instance_child_config(query_data: dict):
        return NodeMgmt().get_instance_child_config(query_data)

    @staticmethod
    def update_instance_child_config(data: dict):
        return NodeMgmt().update_instance_child_config(data)