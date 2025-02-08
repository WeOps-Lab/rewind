COLLECTION_METRICS = {
    "namespace": ["kube_namespace_labels"],
    "workload": [
        "kube_deployment_labels",
        "kube_daemonset_labels",
        "kube_statefulset_labels",
        "kube_job_labels",
        "kube_cronjob_labels",
        "kube_replicaset_labels",
        "kube_replicaset_owner",
    ],
    "node": ["kube_node_info", "kube_node_role", "kube_node_status_capacity"],
    "pod": ["kube_pod_info", "kube_pod_container_resource_limits", "kube_pod_container_resource_requests"],
}

WORKLOAD_TYPE_DICT = {
    "kube_deployment_labels": "deployment",
    "kube_daemonset_labels": "daemonset",
    "kube_statefulset_labels": "statefulset",
    "kube_job_labels": "job",
    "kube_cronjob_labels": "cronjob",
    "kube_replicaset_labels": "replicaset",
}

# workload name dict
WORKLOAD_NAME_DICT = {
    "kube_deployment_labels": "deployment",
    "kube_daemonset_labels": "daemonset",
    "kube_statefulset_labels": "statefulset",
    "kube_job_labels": "job_name",
    "kube_cronjob_labels": "cronjob",
    "kube_replicaset_labels": "replicaset",
}
# namespace与cluster的关联关系
NAMESPACE_CLUSTER_RELATION = "k8s_namespace_belong_k8s_cluster"

# host与cluster的关联关系
NODE_CLUSTER_RELATION = "k8s_node_group_k8s_cluster"

# workload与namespace的关联关系
WORKLOAD_NAMESPACE_RELATION = "k8s_workload_belong_k8s_namespace"

# workload与workload的关联关系
WORKLOAD_WORKLOAD_RELATION = "k8s_workload_group_k8s_workload"

# pod与node的关联关系
POD_NODE_RELATION = "k8s_pod_run_k8s_node"

# pod与workload的关联关系
POD_WORKLOAD_RELATION = "k8s_pod_group_k8s_workload"

# pod与namespace的关联关系
POD_NAMESPACE_RELATION = "k8s_pod_group_k8s_namespace"
