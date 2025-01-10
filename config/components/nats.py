import os

NATS_SERVERS = os.getenv("NATS_SERVERS", "")
NATS_NAMESPACE = os.getenv("NATS_NAMESPACE", "default")
NATS_JETSTREAM_ENABLED = False
