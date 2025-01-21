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

[[outputs.kafka]]
    brokers = ["${DEFAULT_ZONE_VAR_KAFKA_BROKER}"]
    topic = "${DEFAULT_ZONE_VAR_KAFKA_TOPIC}"
    sasl_username = "${DEFAULT_ZONE_VAR_KAFKA_USERNAME}"
    sasl_password = "${DEFAULT_ZONE_VAR_KAFKA_KAFKA_PASSWORD}"
    sasl_mechanism = "PLAIN"
    max_message_bytes = 10000000
    compression_codec=1

[[inputs.internal]]
    tags = { "instance_id"="${node.ip}-${node.cloud_region}","instance_type"="internal","instance_name"="${node.name}" }
"""

# kafka
DEFAULT_ZONE_VAR_KAFKA_BROKER=os.getenv("DEFAULT_ZONE_VAR_KAFKA_BROKER")
DEFAULT_ZONE_VAR_KAFKA_TOPIC=os.getenv("DEFAULT_ZONE_VAR_KAFKA_TOPIC")
DEFAULT_ZONE_VAR_KAFKA_USERNAME=os.getenv("DEFAULT_ZONE_VAR_KAFKA_USERNAME")
DEFAULT_ZONE_VAR_KAFKA_KAFKA_PASSWORD=os.getenv("DEFAULT_ZONE_VAR_KAFKA_KAFKA_PASSWORD")
