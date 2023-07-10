import asyncio
import socket
import ssl

from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

UART_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UART_RX_CHAR_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
UART_TX_CHAR_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'


def sliced(data: bytes, n: int) -> Iterator[bytes]:
    return takewhile(len, (data[i: i + n] for i in count(0, n)))


class BleSocket:
    def __init__(self, client, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP, fileno=1):
        self.__receive_buffer = b''
        self.client = client
        self.family = family
        self.type = type
        self.proto = proto
        self._fileno = fileno

    def __handle_rx(self, _: BleakGATTCharacteristic, data: bytearray):
        print(f'received {len(data)} bytes')
        self.__receive_buffer += data

    @classmethod
    async def create(cls, client: BleakClient):
        self = cls(client)
        await client.start_notify(UART_TX_CHAR_UUID, self.__handle_rx)
        return self

    def send(self, data, flags=0):
        print('sending ', data)
        services = self.client.services.get_service(UART_SERVICE_UUID)
        rx_char = services.get_characteristic(UART_RX_CHAR_UUID)
        for s in sliced(data, rx_char.max_write_without_response_size):
            asyncio.ensure_future(self.client.write_gatt_char(rx_char, s))

        return len(data)

    def recv(self, bufsize, flags=0):
        message = self.__receive_buffer[:bufsize]
        self.__receive_buffer = self.__receive_buffer[bufsize:]
        print('retrieved', message)
        return message

    def fileno(self):
        return self._fileno

    def detach(self):
        fileno = self._fileno
        self._fileno = -1
        return fileno

    def getsockopt(self, level, optname, buflen=256):
        if optname == ssl.SO_TYPE:
            return ssl.SOCK_STREAM

    def fileno(self):
        return self._fileno


async def main():
    async with BleakClient('dc:b5:68:7d:2c:45') \
            as client:
        print('BLE connected')
        ble_socket = await BleSocket.create(client)

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile='auth/app/certificate.pem', keyfile='auth/app/privatekey.pem')
        context.load_verify_locations(cafile='auth/app/ca_certificate.pem')

        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE

        incoming = ssl.MemoryBIO()
        outgoing = ssl.MemoryBIO()
        ssl_object = context.wrap_bio(incoming=incoming, outgoing=outgoing, server_side=False, server_hostname='DeviceType')

        # handshake
        while True:
            try:
                ssl_object.do_handshake()
                break
            except ssl.SSLWantWriteError:
                output = ble_socket.recv(4096)
                if output:
                    incoming.write(output)
                data = outgoing.read()
                if data:
                    ble_socket.send(data)
                await asyncio.sleep(1)
                
            except ssl.SSLWantReadError:
                data = outgoing.read()
                if data:
                    ble_socket.send(data)
                output = ble_socket.recv(4096)
                if output:
                    incoming.write(output)
                await asyncio.sleep(1)

        print('connected')
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        pass  # device disconnected
