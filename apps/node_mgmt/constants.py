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
    agent_id="${node.ip}"

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
    brokers = ["10.11.25.48:9092"]
    topic = "telegraf"
    sasl_username = "admin"
    sasl_password = "ahsae9daeK9o"
    sasl_mechanism = "PLAIN"
    max_message_bytes = 10000000
    compression_codec=1

[[inputs.internal]]
    tags = { "instance_id"="${node.id}","instance_type"="internal","instance_name"="${node.name}" }
"""