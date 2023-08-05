'''Custom 'publish only' redis client which uses redis PIPELINING

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.

TODO:
    RESP3 support (start by sending hello3) / then use hash types
'''

import sys
import asyncio
from urllib.parse import urlparse

import hiredis


class RedisClient(object):
    '''
    See https://redis.io/topics/mass-insert
    '''

    def __init__(self, url, password, verbose=False):

        netloc = urlparse(url).netloc
        host, _, port = netloc.partition(':')
        if port:
            port = int(port)
        else:
            port = 6379

        self.host = host
        self.port = port

        self.password = password
        self.verbose = verbose
        self.lock = asyncio.Lock()

        self._reader = hiredis.Reader()

        self.reader = None
        self.writer = None

        self.read_size = 16 * 1024

    async def connect(self):
        async with self.lock:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )

            if self.password:
                await self.auth(self.password)

    async def readResponse(self):
        response = self._reader.gets()
        while response is False:
            try:
                buf = await self.reader.read(self.read_size)
            except asyncio.CancelledError:
                raise
            except Exception:
                e = sys.exc_info()[1]
                raise ConnectionError(
                    "Error {} while reading from stream: {}".format(type(e), e.args)
                )
            if not buf:
                raise ConnectionError("Socket closed on remote end")
            self._reader.feed(buf)
            response = self._reader.gets()

        return response

    def close(self):
        try:
            if self.writer.can_write_eof():
                self.writer.write_eof()
        except Exception:
            pass

        self.writer.close()

    def writeString(self, data):
        '''
        data should have a type for string or bytes
        '''
        # import pdb; pdb.set_trace()
        # data = data.encode('utf-8')

        self.writer.write(b'$%d\r\n' % len(data))

        if not isinstance(data, bytes):
            self.writer.write(data.encode())
        else:
            self.writer.write(data)

        self.writer.write(b'\r\n')

    async def send(self, cmd, key=None, *args):
        ''' key will be used by redis cluster '''

        if args is None:
            self.writer.write(cmd.encode() + b'\r\n')
        else:
            size = len(args) + 1
            s = f'*{size}\r\n'
            self.writer.write(s.encode())

            self.writeString(cmd)
            for arg in args:
                self.writeString(arg)

        await self.writer.drain()

        response = await self.readResponse()
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
