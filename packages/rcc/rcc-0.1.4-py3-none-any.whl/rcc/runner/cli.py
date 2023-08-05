'''CLI

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio

import click
from rcc.client import RedisClient


async def interpreter(redis_url, redis_password, args):
    client = RedisClient(redis_url, redis_password)
    await client.connect()

    quit = False

    while not quit:
        if len(args) == 0:
            line = input('> ')
            args = line.split()
        else:
            quit = True

        cmd = args[0]
        cmd = cmd.upper()

        if cmd == 'DEL':
            key = args[1]
            response = await client.delete(key)

        elif cmd == 'PING':
            response = await client.ping()
            response = response.decode()

        elif cmd == 'SET':
            key = args[1]
            value = args[2]
            response = await client.set(key, value)
            response = response.decode()

        elif cmd == 'GET':
            key = args[1]
            response = await client.get(key)
            response = response.decode()

        elif cmd == 'EXISTS':
            key = args[1]
            response = await client.exists(key)

        elif cmd == 'XREVRANGE':
            key = args[1]
            end = args[2]
            start = args[3]
            _ = args[4]  # COUNT
            count = args[5]
            response = await client.xrevrange(key, end, start, count)

        print(response)


@click.command()
@click.option('--redis_url', default='redis://localhost')
@click.option('--redis_password')
@click.argument('args', nargs=-1, required=False)
def cli(redis_url, redis_password, args):
    '''Publish to a channel
    '''

    asyncio.get_event_loop().run_until_complete(
        interpreter(redis_url, redis_password, args)
    )
