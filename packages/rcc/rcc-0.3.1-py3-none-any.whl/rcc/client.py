'''Simple client for redis

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.

TODO:
    RESP3 support (start by sending hello3) / then use hash types
'''

import asyncio
import hiredis

from rcc.connection import Connection


class RedisClient(object):
    '''
    See https://redis.io/topics/mass-insert
    '''

    def __init__(self, url, password, verbose=False):
        self.verbose = verbose
        self.password = password

        self.connection = Connection(url, password, verbose)
        self.lock = asyncio.Lock()

        self.hashSlots = {}

    async def connect(self):
        await self.connection.connect()

    async def readResponse(self):
        response = await self.connection.readResponse()
        return response

    def close(self):
        self.connection.close()

    async def send(self, cmd, key=None, *args):
        # FIXME we need a timeout here, and not retry until the end of time
        while True:
            await self.connection.send(cmd, key, *args)
            response = await self.readResponse()

            responseType = type(response)
            if responseType != hiredis.ReplyError:
                return response

            responseStr = str(response)
            if responseStr.startswith('MOVED'):
                tokens = responseStr.split()
                hashSlot = tokens[1]
                url = tokens[2]
                url = 'redis://' + url
                self.hashSlots[hashSlot] = url

                self.connection = Connection(url, self.password, self.verbose)
                await self.connection.connect()
            else:
                return response

    async def auth(self, password):
        async with self.lock:
            return await self.send('AUTH', None, password)

    async def ping(self):
        async with self.lock:
            return await self.send('PING')

    async def delete(self, key):
        async with self.lock:
            return await self.send('DEL', key, key)

    async def set(self, key, value):
        async with self.lock:
            return await self.send('SET', key, key, value)

    async def get(self, key):
        async with self.lock:
            return await self.send('GET', key, key)

    async def exists(self, key):
        async with self.lock:
            return await self.send('EXISTS', key, key)

    async def xinfo(self, key, stream=True):
        async with self.lock:
            return await self.send('XINFO', key, 'STREAM', key)

    async def xadd(self, key: str, attrName: str, attrValue: str, maxLen: int):
        async with self.lock:
            return await self.send(
                'XADD',
                key,
                key,
                b'MAXLEN',
                b'~',
                str(maxLen).encode(),
                b'*',
                attrName,
                attrValue,
            )

    async def xread(self, key, latest_id):
        '''
        Result set is a list
        [[b'1580684995724-0', [b'temperature', b'10']]]
        '''
        async with self.lock:
            response = await self.send(
                'XREAD', key, b'BLOCK', b'0', b'STREAMS', key, latest_id
            )

            items = []
            for item in response[0][1]:
                position = item[0]
                array = item[1]
                entries = {}

                for i in range(len(array) // 2):
                    key = array[2 * i]
                    value = array[2 * i + 1]
                    entries[key] = value

                items.append((position, entries))

            return items

    async def xrevrange(self, key, end, start, count):
        '''
        > XREVRANGE foo + - COUNT 1
        1) 1) "1580792642251-0"
           2) 1) "json"
              2) "{}"
        '''
        async with self.lock:
            response = await self.send(
                'XREVRANGE', key, key, end, start, b'COUNT', str(count)
            )

            items = []
            for item in response:
                position = item[0]
                array = item[1]
                entries = {}

                for i in range(len(array) // 2):
                    key = array[2 * i]
                    value = array[2 * i + 1]
                    entries[key] = value

                items.append((position, entries))

            return items

    def __repr__(self):
        return f'RedisClient at {self.host}:{self.port}'


async def create_redis_publisher(host, port, password, verbose=False):
    client = RedisClient(host, port, password, verbose)
    await client.connect()
    return client
