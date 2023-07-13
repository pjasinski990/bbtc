import asyncio
import socket
import ssl
import sys

from itertools import count, takewhile
from typing import Iterator

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

import tcat_tlv
from ble_stream import BleStream
from ble_stream_secure import BleStreamSecure

UART_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UART_TX_CHAR_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UART_RX_CHAR_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'


dataset = bytes([
    0x0e, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x12, 0x35,
    0x06, 0x00, 0x04, 0x00, 0x1f, 0xff, 0xe0, 0x02,
    0x08, 0xef, 0x13, 0x98, 0xc2, 0xfd, 0x50, 0x4b,
    0x67, 0x07, 0x08, 0xfd, 0x35, 0x34, 0x41, 0x33,
    0xd1, 0xd7, 0x3e, 0x05, 0x10, 0xfd, 0xa7, 0xc7,
    0x71, 0xa2, 0x72, 0x02, 0xe2, 0x32, 0xec, 0xd0,
    0x4c, 0xf9, 0x34, 0xf4, 0x76, 0x03, 0x0f, 0x4f,
    0x70, 0x65, 0x6e, 0x54, 0x68, 0x72, 0x65, 0x61,
    0x64, 0x2d, 0x63, 0x36, 0x34, 0x65, 0x01, 0x02,
    0xc6, 0x4e, 0x04, 0x10, 0x5e, 0x9b, 0x9b, 0x36,
    0x0f, 0x80, 0xb8, 0x8b, 0xe2, 0x60, 0x3f, 0xb0,
    0x13, 0x5c, 0x8d, 0x65, 0x0c, 0x04, 0x02, 0xa0,
    0xf7, 0xf8])


async def main():
    async with await BleStream.create('dc:b5:68:7d:2c:45', UART_SERVICE_UUID, UART_TX_CHAR_UUID, UART_RX_CHAR_UUID) \
            as ble_stream:
        ble_sstream = BleStreamSecure(ble_stream)
        ble_sstream.load_cert(certfile='auth/app/certificate.pem', keyfile='auth/app/privatekey.pem', cafile='auth/app/ca_certificate.pem')
        await ble_sstream.do_handshake('DeviceType')

        print('commissioning')
        data = tcat_tlv.TcatTLV(tcat_tlv.TcatTLV.Type.ACTIVE_DATASET, dataset).to_bytes()
        await ble_sstream.send(data)

        print('sending hello world')
        data = tcat_tlv.TcatTLV(tcat_tlv.TcatTLV.Type.APPLICATION, bytes('hello_world', 'ascii')).to_bytes()
        await ble_sstream.send(data)

        response = await ble_sstream.recv(4096, timeout=1)
        tlv_response = tcat_tlv.TcatTLV.from_bytes(response)
        print('hello world response:', tlv_response.type, tlv_response.data)

        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        pass  # device disconnected
