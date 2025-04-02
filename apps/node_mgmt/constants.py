import os

NORMAL = "normal"
ABNORMAL = "abnormal"
NOT_INSTALLED = "not_installed"

SIDECAR_STATUS_ENUM = {
    NORMAL: "正常",
    ABNORMAL: "异常",
    NOT_INSTALLED: "未安装",
}

# 本服务的地址
LOCAL_HOST = os.getenv("WEB_SERVER_URL")

LINUX_OS = "linux"
WINDOWS_OS = "windows"

W_SIDECAR_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=sidecar_windows.zip"
L_SIDECAR_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=sidecar_linux.tar.gz"
L_INSTALL_DOWNLOAD_URL = f"{LOCAL_HOST}/openapi/sidecar/download_file/?file_name=install_sidecar.sh"

default_sidecar_mode = os.getenv("SIDECAR_INPUT_MODE", "telegraf")
TELEGRAF_CONFIG = """
[global_tags]
    agent_id="${node.ip}-${node.cloud_region}"

[agent]
    interval = "10s"
    round_interval = true
    metric_batch_size = 1000
    metric_buffer_limit = 10000
    collection_jitter = "0s"
    flush_interval = "30s"
    flush_jitter = "0s"
    precision = "0s"
    hostname = "${node.ip}"
    omit_hostname = false

[[inputs.internal]]
    tags = { "instance_id"="${node.ip}-${node.cloud_region}","instance_type"="internal","instance_name"="${node.name}" }
"""

if default_sidecar_mode == "telegraf":
    TELEGRAF_CONFIG += """
[[outputs.kafka]]
brokers = ["${KAFKA_HOST}:${KAFKA_PORT}"]
topic = "${KAFKA_METRICS_TOPIC}"
sasl_username = "${KAFKA_USERNAME}"
sasl_password = "${KAFKA_PASSWORD}"
sasl_mechanism = "PLAIN"
max_message_bytes = 10000000
compression_codec=1
"""

if default_sidecar_mode == "nats":
    TELEGRAF_CONFIG += """
[[outputs.nats]]
servers = ["${NATS_SERVERS}"]
username = "${NATS_USERNAME}"
password = "${NATS_PASSWORD}"
subject = "metrics.${node.ip_filter}"
data_format = "influx"
"""

if default_sidecar_mode == "vm":
    TELEGRAF_CONFIG += """
[[outputs.influxdb]]
  urls = ["${VM_SERVERS}"]
  database = "victoriametrics"
  skip_database_creation = true
  exclude_retention_policy_tag = true
  content_encoding = "gzip"
"""  