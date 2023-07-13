import asyncio
import ssl

from ble_stream import BleStream

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
            except ssl.SSLWantWriteError:
                output = self.ble_stream.recv(4096)
                if output:
                    self.incoming.write(output)
                data = self.outgoing.read()
                if data:
                    await self.ble_stream.send(data)
                await asyncio.sleep(1)

            except ssl.SSLWantReadError:
                data = self.outgoing.read()
                if data:
                    await self.ble_stream.send(data)
                output = self.ble_stream.recv(4096)
                if output:
                    self.incoming.write(output)
                await asyncio.sleep(1)


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
        decode = self.ssl_object.read(4096)
        return decode
