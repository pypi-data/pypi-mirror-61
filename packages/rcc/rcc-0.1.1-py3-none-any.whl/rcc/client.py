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
                self.writer.write(b'*2\r\n')
                self.writeString(b'AUTH')

                password = self.password
                if not isinstance(password, bytes):
                    password = password.encode('utf8')

                # FIXME / validate response
                await self.readResponse()

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

    async def send(self, cmd, key=None, args=None):
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

    async def ping(self):
        async with self.lock:
            return await self.send('PING')

    async def set(self, key, value):
        async with self.lock:
            return await self.send('SET', key, [key, value])

    async def get(self, key):
        async with self.lock:
            return await self.send('GET', key, [key])

    async def exists(self, key):
        async with self.lock:
            self.writer.write(b'*2\r\n')
            self.writeString(b'EXISTS')
            self.writeString(key)

            await self.writer.drain()
            response = await self.readResponse()
            return response == 1

    async def xinfo(self, key, stream=True):
        async with self.lock:
            self.writer.write(b'*3\r\n')
            self.writeString(b'XINFO')

            if stream:
                self.writeString(b'STREAM')

            self.writeString(key)

            await self.writer.drain()
            response = await self.readResponse()
            return response

    async def xadd(self, key: str, attrName: str, attrValue: str, maxLen: int):
        async with self.lock:
            self.writer.write(b'*8\r\n')
            self.writeString(b'XADD')
            self.writeString(key)

            # should be optional
            self.writeString(b'MAXLEN')
            self.writeString(b'~')
            self.writeString(str(maxLen).encode())
            self.writeString(b'*')
            self.writeString(attrName)
            self.writeString(attrValue)

            await self.writer.drain()
            response = await self.readResponse()
            return response

    async def xread(self, key, latest_id):
        '''
        Result set is a list
        [[b'1580684995724-0', [b'temperature', b'10']]]
        '''
        async with self.lock:
            self.writer.write(b'*6\r\n')
            self.writeString(b'XREAD')
            self.writeString(b'BLOCK')
            self.writeString(b'0')
            self.writeString(b'STREAMS')
            self.writeString(key)
            self.writeString(latest_id)

            await self.writer.drain()
            response = await self.readResponse()

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
            self.writer.write(b'*6\r\n')
            self.writeString(b'XREVRANGE')
            self.writeString(key)
            self.writeString(end)
            self.writeString(start)
            self.writeString(b'COUNT')
            self.writeString(str(count))

            await self.writer.drain()
            response = await self.readResponse()

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

    async def delete(self, key):
        '''Delete a key
        '''
        async with self.lock:
            self.writer.write(b'*2\r\n')
            self.writeString(b'DEL')
            self.writeString(key)

            await self.writer.drain()
            response = await self.readResponse()
            return response

    def __repr__(self):
        return f'RedisClient at {self.host}:{self.port}'


async def create_redis_publisher(host, port, password, verbose=False):
    client = RedisClient(host, port, password, verbose)
    await client.connect()
    return client
