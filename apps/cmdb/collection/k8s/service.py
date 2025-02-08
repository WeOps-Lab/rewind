from datetime import datetime, timezone

from apps.cmdb.collection.common import Collection, Management
from apps.cmdb.collection.k8s.constants import (
    COLLECTION_METRICS,
    NAMESPACE_CLUSTER_RELATION,
    NODE_CLUSTER_RELATION,
    POD_NAMESPACE_RELATION,
    POD_WORKLOAD_RELATION,
    WORKLOAD_NAME_DICT,
    WORKLOAD_NAMESPACE_RELATION,
    WORKLOAD_TYPE_DICT,
    WORKLOAD_WORKLOAD_RELATION,
)
from apps.cmdb.constants import INSTANCE
from apps.cmdb.graph.neo4j import Neo4jClient


# 指标纳管（纳管控制器）
class MetricsCannula:
    def __init__(self, organization: list, cluster_name: str):
        self.organization = organization
        self.cluster_name = cluster_name
        self.collection_metrics = self.get_collection_metrics()
        self.now_time = datetime.now(timezone.utc).isoformat()

    def get_collection_metrics(self):
        """获取采集指标"""
        new_metrics = CollectMetrics(self.cluster_name)
        return new_metrics.run()

    def namespace_controller(self):
        """namespace控制器"""
        params = [
            {"field": "model_id", "type": "str=", "value": "k8s_namespace"},
            {"field": "collect_task", "type": "str=", "value": self.cluster_name},
        ]
        with Neo4jClient() as ag:
            already_namespace, _ = ag.query_entity(INSTANCE, params)

        return Management(
            self.organization,
            self.cluster_name,
            "k8s_namespace",
            already_namespace,
            self.collection_metrics["namespace"],
            ["inst_name"],
            self.now_time,
        ).controller()

    def workload_controller(self):
        """workload控制器"""
        params = [
            {"field": "model_id", "type": "str=", "value": "k8s_workload"},
            {"field": "collect_task", "type": "str=", "value": self.cluster_name},
        ]
        with Neo4jClient() as ag:
            already_workload, _ = ag.query_entity(INSTANCE, params)

        return Management(
            self.organization,
            self.cluster_name,
            "k8s_workload",
            already_workload,
            self.collection_metrics["workload"],
            ["inst_name"],
            self.now_time,
        ).controller()

    def pod_controller(self):
        """pod控制器"""
        params = [
            {"field": "model_id", "type": "str=", "value": "k8s_pod"},
            {"field": "collect_task", "type": "str=", "value": self.cluster_name},
        ]
        with Neo4jClient() as ag:
            already_pod, _ = ag.query_entity(INSTANCE, params)
        return Management(
            self.organization,
            self.cluster_name,
            "k8s_pod",
            already_pod,
            self.collection_metrics["pod"],
            ["inst_name"],
            self.now_time,
        ).controller()

    def node_controller(self):
        """node控制器"""
        params = [
            {"field": "model_id", "type": "str=", "value": "k8s_node"},
            {"field": "collect_task", "type": "str=", "value": self.cluster_name},
        ]
        with Neo4jClient() as ag:
            already_node, _ = ag.query_entity(INSTANCE, params)
        return Management(
            self.organization,
            self.cluster_name,
            "k8s_node",
            already_node,
            self.collection_metrics["node"],
            ["inst_name"],
            self.now_time,
        ).controller()

    def cannula_controller(self):
        """纳管控制器"""
        k8s_node = self.node_controller()
        k8s_namespace = self.namespace_controller()
        k8s_workload = self.workload_controller()
        k8s_pod = self.pod_controller()
        return dict(node=k8s_node, namespace=k8s_namespace, workload=k8s_workload, pod=k8s_pod)


# 指标采集处理（指标查询、指标格式化）
class CollectMetrics:
    def __init__(self, cluster_name):
        self.cluster_name = cluster_name
        self.metrics = self.get_metrics()
        self.collection_metrics_dict = {i: [] for i in COLLECTION_METRICS.keys()}

    def get_metrics(self):
        metrics = []
        metrics.extend(COLLECTION_METRICS["namespace"])
        metrics.extend(COLLECTION_METRICS["workload"])
        metrics.extend(COLLECTION_METRICS["node"])
        metrics.extend(COLLECTION_METRICS["pod"])
        return metrics

    def query_data(self):
        """查询数据"""
        sql = f"""
        WITH latest_time AS (
            SELECT max(TimeUnix) AS latest_timestamp
            FROM otel.otel_metrics_gauge
            WHERE MetricName IN {self.metrics}
            AND Attributes['instance_id'] = '{self.cluster_name}'
        )
        SELECT
            MetricName, Attributes, TimeUnix, Value
        FROM
            otel.otel_metrics_gauge
        WHERE
            MetricName IN {self.metrics}
            AND Attributes['instance_id'] = '{self.cluster_name}'
            AND TimeUnix = (SELECT latest_timestamp FROM latest_time)
        FORMAT JSON
        """
        data = Collection().query(sql)
        return data.get("data", [])

    def format_data(self, data):
        """格式化数据"""

        for index_data in data:
            index_dict = dict(
                index_key=index_data["MetricName"],
                index_value=index_data["Value"],
                index_time=index_data["TimeUnix"],
                **index_data["Attributes"],
            )
            if index_data["MetricName"] in COLLECTION_METRICS["namespace"]:
                self.collection_metrics_dict["namespace"].append(index_dict)
            elif index_data["MetricName"] in COLLECTION_METRICS["workload"]:
                self.collection_metrics_dict["workload"].append(index_dict)
            elif index_data["MetricName"] in COLLECTION_METRICS["node"]:
                self.collection_metrics_dict["node"].append(index_dict)
            elif index_data["MetricName"] in COLLECTION_METRICS["pod"]:
                self.collection_metrics_dict["pod"].append(index_dict)

        self.format_namespace_metrics()
        self.format_pod_metrics()
        self.format_node_metrics()
        self.format_workload_metrics()

    def format_namespace_metrics(self):
        """格式化namespace"""
        result = []
        for index_data in self.collection_metrics_dict["namespace"]:
            result.append(
                dict(
                    inst_name=f"{index_data['instance_id']}/{index_data['namespace']}",
                    name=index_data["namespace"],
                    assos=[
                        {
                            "model_id": "k8s_cluster",
                            "inst_name": self.cluster_name,
                            "asst_id": "belong",
                            "model_asst_id": NAMESPACE_CLUSTER_RELATION,
                        }
                    ],
                )
            )
        self.collection_metrics_dict["namespace"] = result

    def format_workload_metrics(self):
        """格式化workload"""
        replicaset_owner_dict, replicaset_metrics, workload_metrics = {}, [], []
        for index_data in self.collection_metrics_dict["workload"]:
            if index_data["index_key"] == "kube_replicaset_labels":
                replicaset_metrics.append(index_data)
            elif index_data["index_key"] == "kube_replicaset_owner":
                replicaset_owner_dict[(index_data["namespace"], index_data["replicaset"])] = index_data
            else:
                workload_metrics.append(index_data)
        for replicaset_info in replicaset_metrics:
            owner_info = replicaset_owner_dict.get((replicaset_info["namespace"], replicaset_info["replicaset"]))
            if owner_info and owner_info["owner_kind"].lower() in WORKLOAD_TYPE_DICT.values():
                replicaset_info.update(
                    owner_kind=owner_info["owner_kind"].lower(),
                    owner_name=owner_info["owner_name"],
                )
        workload_metrics.extend(replicaset_metrics)
        result = []
        for workload_info in workload_metrics:
            inst_name_key = WORKLOAD_NAME_DICT[workload_info["index_key"]]
            namespase = f"{workload_info['instance_id']}/{workload_info['namespace']}"
            if workload_info.get("owner_kind"):
                # 关联workload
                assos = [
                    {
                        "model_id": "k8s_workload",
                        "inst_name": f"{namespase}/{workload_info['owner_name']}",
                        "asst_id": "group",
                        "model_asst_id": WORKLOAD_WORKLOAD_RELATION,
                    }
                ]
            else:
                # 关联namespace
                workload_info.update(k8s_namespace=namespase)
                assos = [
                    {
                        "model_id": "k8s_namespace",
                        "inst_name": namespase,
                        "asst_id": "belong",
                        "model_asst_id": WORKLOAD_NAMESPACE_RELATION,
                    }
                ]

            result.append(
                dict(
                    inst_name=f"{workload_info['instance_id']}/{workload_info['namespace']}/{workload_info[inst_name_key]}",  # noqa
                    name=workload_info[inst_name_key],
                    workload_type=WORKLOAD_TYPE_DICT[workload_info["index_key"]],
                    assos=assos,
                )
            )

        self.collection_metrics_dict["workload"] = result

    def format_pod_metrics(self):
        """格式化pod"""
        inst_index_info_list, inst_limit_resource_dict, inst_request_resource_dict = [], {}, {}
        for index_data in self.collection_metrics_dict["pod"]:
            if index_data["index_key"] == "kube_pod_info":
                inst_index_info_list.append(index_data)
            elif index_data["index_key"] == "kube_pod_container_resource_limits":
                inst_limit_resource_dict[(index_data["pod"], index_data["resource"])] = index_data["index_value"]
            elif index_data["index_key"] == "kube_pod_container_resource_requests":
                inst_request_resource_dict[(index_data["pod"], index_data["resource"])] = index_data["index_value"]

        result = []
        for inst_index_info in inst_index_info_list:
            namespase = f"{inst_index_info['instance_id']}/{inst_index_info['namespace']}"

            info = dict(
                inst_name=inst_index_info["uid"],
                name=inst_index_info["pod"],
                ip_addr=inst_index_info["pod_ip"],
            )

            limit_cpu = inst_limit_resource_dict.get((inst_index_info["pod"], "cpu"))
            if limit_cpu:
                info.update(limit_cpu=float(limit_cpu))
            limit_memory = inst_limit_resource_dict.get((inst_index_info["pod"], "memory"))
            if limit_memory:
                info.update(limit_memory=int(float(limit_memory) / 1024**3))
            request_cpu = inst_request_resource_dict.get((inst_index_info["pod"], "cpu"))
            if request_cpu:
                info.update(request_cpu=float(request_cpu))
            request_memory = inst_request_resource_dict.get((inst_index_info["pod"], "memory"))
            if request_memory:
                info.update(request_memory=int(float(request_memory) / 1024**3))

            assos = [
                {
                    "model_id": "k8s_node",
                    "inst_name": f"{inst_index_info['instance_id']}/{inst_index_info['node']}",
                    "asst_id": "group",
                    "model_asst_id": POD_WORKLOAD_RELATION,
                }
            ]

            if inst_index_info["created_by_kind"] in WORKLOAD_TYPE_DICT.values():
                # 关联workload
                inst_index_info.update(k8s_workload=f"{inst_index_info['created_by_name']}")
                assos.append(
                    {
                        "model_id": "k8s_workload",
                        "inst_name": f"{namespase}/{inst_index_info['created_by_name']}",
                        "asst_id": "group",
                        "model_asst_id": POD_WORKLOAD_RELATION,
                    }
                )
            else:
                # 关联namespace
                inst_index_info.update(k8s_namespace=namespase)
                assos.append(
                    {
                        "model_id": "k8s_namespace",
                        "inst_name": namespase,
                        "asst_id": "group",
                        "model_asst_id": POD_NAMESPACE_RELATION,
                    }
                )
            info.update(assos=assos)
            result.append(info)

        self.collection_metrics_dict["pod"] = result

    def format_node_metrics(self):
        """格式化node"""
        inst_index_info_list, inst_resource_dict, inst_role_dict = [], {}, {}
        for index_data in self.collection_metrics_dict["node"]:
            if index_data["index_key"] == "kube_node_info":
                inst_index_info_list.append(index_data)
            elif index_data["index_key"] == "kube_node_role":
                if index_data["node"] not in inst_role_dict:
                    inst_role_dict[index_data["node"]] = []
                inst_role_dict[index_data["node"]].append(index_data["role"])
            elif index_data["index_key"] == "kube_node_status_capacity":
                inst_resource_dict[(index_data["node"], index_data["resource"])] = index_data["index_value"]
        result = []
        for inst_index_info in inst_index_info_list:
            info = dict(
                inst_name=f"{inst_index_info['instance_id']}/{inst_index_info['node']}",
                name=inst_index_info["node"],
                ip_addr=inst_index_info.get("internal_ip"),
                os_version=inst_index_info.get("os_image"),
                kernel_version=inst_index_info.get("kernel_version"),
                kubelet_version=inst_index_info.get("kubelet_version"),
                container_runtime_version=inst_index_info.get("container_runtime_version"),
                pod_cidr=inst_index_info.get("pod_cidr"),
                assos=[
                    {
                        "model_id": "k8s_cluster",
                        "inst_name": self.cluster_name,
                        "asst_id": "group",
                        "model_asst_id": NODE_CLUSTER_RELATION,
                    }
                ],
            )
            info = {k: v for k, v in info.items() if v}
            cpu = inst_resource_dict.get((inst_index_info["node"], "cpu"))
            if cpu:
                info.update(cpu=int(cpu))
            memory = inst_resource_dict.get((inst_index_info["node"], "memory"))
            if memory:
                info.update(memory=int(float(memory) / 1024**3))
            disk = inst_resource_dict.get((inst_index_info["node"], "ephemeral_storage"))
            if disk:
                info.update(storage=int(float(disk) / 1024**3))
            role = ",".join(inst_role_dict.get(inst_index_info["node"], []))
            if role:
                info.update(role=role)
            result.append(info)
        self.collection_metrics_dict["node"] = result

    def run(self):
        """执行"""
        data = self.query_data()
        self.format_data(data)
        return self.collection_metrics_dict
