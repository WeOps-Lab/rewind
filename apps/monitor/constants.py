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
        "default_metric": 'any({instance_type="os"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["cpu_summary.usage", "mem.pct_used", "load5"],
    },
    {
        "type": "Web",
        "name": "Website",
        "default_metric": 'any({instance_type="web"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["http_duration", "http_success.rate"],
    },
    {
        "type": "Web",
        "name": "Ping",
        "default_metric": 'any({instance_type="ping"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["ping_response_time", "ping_error_response_code"],
    },
    {
        "type": "Network Device",
        "name": "Switch",
        "default_metric": 'any({instance_type="switch"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Network Device",
        "name": "Router",
        "default_metric": 'any({instance_type="router"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Network Device",
        "name": "Firewall",
        "default_metric": 'any({instance_type="firewall"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Network Device",
        "name": "Loadbalance",
        "default_metric": 'any({instance_type="loadbalance"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Network Device",
        "name": "Detection Device",
        "default_metric": 'any({instance_type="detection_device"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Network Device",
        "name": "Scanning Device",
        "default_metric": 'any({instance_type="scanning_device"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Hardware Device",
        "name": "Bastion Host",
        "default_metric": 'any({instance_type="bastion_host"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Hardware Device",
        "name": "Storage",
        "default_metric": 'any({instance_type="storage"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "Hardware Device",
        "name": "Hardware Server",
        "default_metric": 'any({instance_type="hardware_server"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["sysUpTime", "iftotalInOctets", "iftotalOutOctets"],
    },
    {
        "type": "K8S",
        "name": "Cluster",
        "default_metric": 'any({instance_type="k8s"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": ["cluster_pod_count", "cluster_node_count"],
    },
    {
        "type": "K8S",
        "name": "Pod",
        "default_metric": 'prometheus_remote_write_kube_pod_container_info',
        "instance_id_keys": ["pod"],
        "supplementary_indicators": ["pod_status", "pod_cpu_utilization","pod_memory_utilization"],
    },
    {
        "type": "K8S",
        "name": "Node",
        "default_metric": 'prometheus_remote_write_kube_node_info',
        "instance_id_keys": ["node"],
        "supplementary_indicators": ["node_status_condition", "node_cpu_utilization", "node_memory_utilization"],
    },
    {
        "type": "Other",
        "name": "SNMP Trap",
        "default_metric": 'any({instance_type="snmp_trap"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
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
    "warning": 2,
    "error": 3,
    "critical": 4,
    "no_data": 5,
}