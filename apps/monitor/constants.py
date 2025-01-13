import os

# victoriametrics服务信息
VICTORIAMETRICS_HOST = os.getenv("VICTORIAMETRICS_HOST")
VICTORIAMETRICS_USER = os.getenv("VICTORIAMETRICS_USER")
VICTORIAMETRICS_PWD = os.getenv("VICTORIAMETRICS_PWD")

# 内置的监控对象
MONITOR_OBJS = [
    {
        "type": "OS",
        "name": "Host",
        "default_metric": 'system_load1{instance_type="os"}',
        "instance_id_key": "instance_id",
        "instance_name_key": "host",
        "supplementary_indicators": ["cpu_summary.usage", "mem.pct_usable", "load5"],
    },
    {
        "type": "Web",
        "name": "Website",
        "default_metric": "probe_duration_seconds_gauge",
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["http_success.rate", "http_total.duration"],
    },
    {
        "type": "K8S",
        "name": "Cluster",
        "default_metric": 'internal_write_write_time_ns{instance_type="k8s"}',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["cluster_pod_count", "cluster_node_count"],
    },
    {
        "type": "K8S",
        "name": "Pod",
        "default_metric": 'prometheus_remote_write_kube_pod_container_info',
        "instance_id_key": "pod",
        "instance_name_key": "pod",
        "supplementary_indicators": ["pod_status", "pod_cpu_utilization","pod_memory_utilization"],
    },
    {
        "type": "K8S",
        "name": "Node",
        "default_metric": 'prometheus_remote_write_kube_node_info',
        "instance_id_key": "node",
        "instance_name_key": "node",
        "supplementary_indicators": ["node_status_condition", "node_cpu_utilization", "node_memory_utilization"],
    },
    {
        "type": "Device",
        "name": "Switch",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="swtich"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Router",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="router"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Firewall",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="firewall"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Loadbalance",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="loadbalance"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Bastion Host",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="bastion_host"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Detection Device",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="detection_device"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Device",
        "name": "Scanning Device",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="scanning_device"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "System",
        "name": "Audit System",
        "default_metric": 'cw_CommonNetwork_sysUpTime_gauge{instance_type="audit_system"} /60/60/24',
        "instance_id_key": "instance_id",
        "instance_name_key": "instance_name",
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
]

# 阀值对比方法
THRESHOLD_METHODS = {
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    "=": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
}

# 告警等级权重
LEVEL_WEIGHT = {
    "info": 1,
    "warning": 2,
    "error": 3,
    "critical": 4,
    "no_data": 5,
}