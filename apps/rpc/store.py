import logging
import os
import nats
from nats.js.api import ObjectMeta
from nats.js.errors import BucketNotFoundError

logger = logging.getLogger("app")


class JetStreamObjectStore:
    def __init__(self, servers=None, bucket_name='configs'):
        self.servers = servers or os.environ.get('NATS_URL', 'nats://localhost:4222').split(',')
        self.bucket_name = bucket_name
        self.nc = None
        self.js = None
        self.object_store = None

    async def connect(self):
        self.nc = await nats.connect(servers=self.servers)
        self.js = self.nc.jetstream()
        try:
            self.object_store = await self.js.object_store(self.bucket_name)
        except BucketNotFoundError:
            self.object_store = await self.js.create_object_store(self.bucket_name)
        logger.info(f'Connected to NATS and initialized object store: {self.bucket_name}')

    async def put(self, key, data, description=None):
        meta = ObjectMeta(description=description) if description else None
        info = await self.object_store.put(key, data, meta=meta)
        logger.info(f'Added entry {info.name} ({info.size} bytes)')
        return info

    async def get(self, key):
        result = await self.object_store.get(key)
        logger.info(f'Fetched entry {result.info.name} ({result.info.size} bytes)')
        return result.data

    async def delete(self, key):
        await self.object_store.delete(key)
        logger.info(f'Deleted entry {key}')

    async def list_objects(self):
        entries = await self.object_store.list()
        logger.info(f'The object store contains {len(entries)} entries')
        return entries

    async def watch_updates(self):
        watcher = await self.object_store.watch(include_history=False)
        while True:
            e = await watcher.updates()
            if e:
                update_type = 'deleted' if e.deleted else 'updated'
                logger.info(f'{self.bucket_name} changed - {e.name} was {update_type}')

    async def close(self):
        await self.nc.close()
        logger.info('Closed connection to NATS')


# 示例用法
# async def main():
#     store = JetStreamObjectStore()
#     await store.connect()
#
#     # 上传对象
#     await store.put('example.txt', b'Hello, NATS!', description='Test file')
#
#     # 下载对象
#     data = await store.get('example.txt')
#     print(f'Downloaded content: {data.decode()}')
#
#     # 列出对象
#     await store.list_objects()
#
#     # 删除对象
#     await store.delete('example.txt')
#
#     # 关闭连接
#     await store.close()
