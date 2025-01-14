import asyncio
import json

import nats_client


class RpcClient(object):
    def __init__(self, namespace):
        self.namespace = namespace

    def run(self, method_name, *args, **kwargs):
        return_data = asyncio.run(nats_client.request(
            self.namespace,
            method_name,
            *args,
            **kwargs
        ))
        return json.loads(return_data)
