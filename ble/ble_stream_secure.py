"""
   Copyright (c) 2023 Nordic Semiconductor ASA

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import asyncio
import ssl

from .ble_stream import BleStream

class BleStreamSecure:
    def __init__(self, ble_stream: BleStream):
        self.ble_stream = ble_stream
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.incoming = ssl.MemoryBIO()
        self.outgoing = ssl.MemoryBIO()
        self.ssl_object = None


    def load_cert(self, certfile='', keyfile='', cafile=''):
        if certfile and keyfile:
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        elif certfile:
            self.ssl_context.load_cert_chain(certfile=certfile)

        if cafile:
            self.ssl_context.load_verify_locations(cafile=cafile)


    async def do_handshake(self, hostname):
        self.ssl_object = self.ssl_context.wrap_bio(incoming=self.incoming, outgoing=self.outgoing, server_side=False, server_hostname=hostname)
        while True:
            try:
                self.ssl_object.do_handshake()
                break
            # SSLWantWrite means ssl wants to send data over the link, but might need a receive first
            except ssl.SSLWantWriteError:
                output = self.ble_stream.recv(4096)
                if output:
                    self.incoming.write(output)
                data = self.outgoing.read()
                if data:
                    await self.ble_stream.send(data)
                await asyncio.sleep(0.1)

            # SSLWantWrite means ssl wants to receive data from the link, but might need to send first
            except ssl.SSLWantReadError:
                data = self.outgoing.read()
                if data:
                    await self.ble_stream.send(data)
                output = self.ble_stream.recv(4096)
                if output:
                    self.incoming.write(output)
                await asyncio.sleep(0.1)


    async def send(self, bytes):
        self.ssl_object.write(bytes)
        encode = self.outgoing.read(4096)
        await self.ble_stream.send(encode)


    async def recv(self, buffersize, timeout=0):
        end_time = asyncio.get_event_loop().time() + timeout
        data = self.ble_stream.recv(buffersize)
        while not data and asyncio.get_event_loop().time() < end_time:
            await asyncio.sleep(0.1)
            data = self.ble_stream.recv(buffersize)
        if not data:
            return b''

        self.incoming.write(data)
        while True:
            try:
                decode = self.ssl_object.read(4096)
                break
            # if recv called before entire message was received from the link
            except ssl.SSLWantReadError:
                more = self.ble_stream.recv(buffersize)
                while not more:
                    await asyncio.sleep(0.1)
                    more = self.ble_stream.recv(buffersize)
                self.incoming.write(more)
        return decode


    async def send_with_resp(self, bytes):
        await self.send(bytes)
        res = await self.recv(4096, timeout=5)
        return res
