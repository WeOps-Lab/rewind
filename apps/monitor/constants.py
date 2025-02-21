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
        "instance_id_keys": ["instance_id", "pod"],
        "supplementary_indicators": ["pod_status", "pod_cpu_utilization","pod_memory_utilization"],
    },
    {
        "type": "K8S",
        "name": "Node",
        "default_metric": 'prometheus_remote_write_kube_node_info',
        "instance_id_keys": ["instance_id", "node"],
        "supplementary_indicators": ["node_status_condition", "node_cpu_utilization", "node_memory_utilization"],
    },
    {
        "type": "Other",
        "name": "SNMP Trap",
        "default_metric": 'any({instance_type="snmp_trap"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "RabbitMQ",
        "default_metric": 'any({instance_type="rabbitmq"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "Nginx",
        "default_metric": 'any({instance_type="nginx"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "Zookeeper",
        "default_metric": 'any({instance_type="zookeeper"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "ActiveMQ",
        "default_metric": 'any({instance_type="activemq"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "Apache",
        "default_metric": 'any({instance_type="apache"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "ClickHouse",
        "default_metric": 'any({instance_type="clickhouse"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Middleware",
        "name": "Consul",
        "default_metric": 'any({instance_type="consul"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Container Management",
        "name": "Docker",
        "default_metric": 'any({instance_type="docker"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Container Management",
        "name": "Docker Container",
        "default_metric": 'docker_container_mem_usage',
        "instance_id_keys": ["instance_id", "container_name"],
        "supplementary_indicators": [],
    },
    {
        "type": "Database",
        "name": "ElasticSearch",
        "default_metric": 'any({instance_type="elasticsearch"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Database",
        "name": "Mysql",
        "default_metric": 'any({instance_type="mysql"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Database",
        "name": "MongoDB",
        "default_metric": 'any({instance_type="mongodb"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Database",
        "name": "Redis",
        "default_metric": 'any({instance_type="redis"}) by (instance_id)',
        "instance_id_keys": ["instance_id"],
        "supplementary_indicators": [],
    },
    {
        "type": "Database",
        "name": "Postgres",
        "default_metric": 'any({instance_type="postgres"}) by (instance_id)',
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