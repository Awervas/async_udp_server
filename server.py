import argparse
import asyncio
import logging
from asyncio import Future
from typing import List

logger = logging.getLogger(__name__)

VERSION = "1.0.0"

class UDPProtocol(asyncio.DatagramProtocol):

    def __init__(self, handler):
        self.transport = None
        self.handler = handler

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data:bytes, addr:tuple):
        self.handler(data, addr)


async def start_udp_server(host, port, handler):
    loop = asyncio.get_running_loop()
    logger.info(f"Starting UDP server {host, port}")
    try:
        transport, _ = await loop.create_datagram_endpoint(
            lambda: UDPProtocol(handler=handler),
            local_addr=(host, port)
        )
    except Exception as e:
        transport = None
        logger.exception(f'error start udp: {e}')

    try:
        while 1:
            await asyncio.sleep(3600)
    finally:
        if transport:
            transport.close()



def print_message(message:bytes, addr:str):
    print(message.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Async UDP server')
    parser.add_argument('-b', '--bind', type=str, default='127.0.0.1')
    parser.add_argument('-p','--port',type=int, required=True)
    parser.add_argument('--version', action='version', version=f"{VERSION}")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_udp_server(args.bind, args.port, print_message))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_udp_server('127.0.0.1', 9999, None))