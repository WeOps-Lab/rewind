import os

# REMOTE_SERVICE
FILE_CHUNK_SERVICE_URL = os.getenv("FILE_CHUNK_SERVICE_URL", "http://chunk-server/file_chunk")
MANUAL_CHUNK_SERVICE_URL = os.getenv("MANUAL_CHUNK_SERVICE_URL", "http://chunk-server/manual_chunk")
WEB_PAGE_CHUNK_SERVICE_URL = os.getenv("WEB_PAGE_CHUNK_SERVICE_URL", "http://chunk-server/webpage_chunk")
OPENAI_CHAT_SERVICE_URL = os.getenv("OPENAI_CHAT_SERVICE_URL", "http://chat-server/openai")
REMOTE_INDEX_URL = os.getenv("REMOTE_INDEX_URL", "http://rag-server/elasticsearch_index")
RAG_SERVER_URL = os.getenv("RAG_SERVER_URL", "http://rag-server/elasticsearch_rag")
ONLINE_SEARCH_SERVER_URL = os.getenv("ONLINE_SEARCH_SERVER_URL", "http://rag-server/online_search")

# BOT 环境变量
KUBE_SERVER_URL = os.getenv("KUBE_SERVER_URL", "http://kube-service.lite")
KUBE_NAMESPACE = os.getenv("KUBE_NAMESPACE", "lite")
KUBE_TOKEN = os.getenv("KUBE_TOKEN", "")

MUNCHKIN_BASE_URL = os.getenv("MUNCHKIN_BASE_URL", "http://munchkin")

CONVERSATION_MQ_HOST = os.getenv("CONVERSATION_MQ_HOST", "rabbitmq.ops-pilot")
CONVERSATION_MQ_PORT = int(os.getenv("CONVERSATION_MQ_PORT", 5672))
CONVERSATION_MQ_USER = os.getenv("CONVERSATION_MQ_USER", "admin")
CONVERSATION_MQ_PASSWORD = os.getenv("CONVERSATION_MQ_PASSWORD", "password")


# ES 配置
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

# MINIO 配置
MINIO_PRIVATE_BUCKETS = ["munchkin-private"]
MINIO_PUBLIC_BUCKETS = ["munchkin-public"]
