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

from itertools import count, takewhile
from typing import Iterator
import logging

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

logger = logging.getLogger(__name__)
class BleStream:
    def __init__(self, client, service_uuid, tx_char_uuid, rx_char_uuid):
        self.__receive_buffer = b''
        self.client = client
        self.service_uuid = service_uuid
        self.tx_char_uuid = tx_char_uuid
        self.rx_char_uuid = rx_char_uuid


    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.client.is_connected:
            await self.client.disconnect()


    def __handle_rx(self, _: BleakGATTCharacteristic, data: bytearray):
        logger.debug(f'received {len(data)} bytes')
        self.__receive_buffer += data


    @staticmethod
    def __sliced(data: bytes, n: int) -> Iterator[bytes]:
        return takewhile(len, (data[i: i + n] for i in count(0, n)))


    @classmethod
    async def create(cls, address, service_uuid, tx_char_uuid, rx_char_uuid):
        client = BleakClient(address)
        await client.connect()
        self = cls(client, service_uuid, tx_char_uuid, rx_char_uuid)
        await client.start_notify(self.tx_char_uuid, self.__handle_rx)
        return self


    async def send(self, data):
        logger.debug(f'sending {data}')
        services = self.client.services.get_service(self.service_uuid)
        rx_char = services.get_characteristic(self.rx_char_uuid)
        for s in BleStream.__sliced(data, rx_char.max_write_without_response_size):
            await self.client.write_gatt_char(rx_char, s)
        return len(data)


    def recv(self, bufsize, flags=0):
        if not self.__receive_buffer:
            return b''
        message = self.__receive_buffer[:bufsize]
        self.__receive_buffer = self.__receive_buffer[bufsize:]
        logger.debug(f'retrieved {message}')
        return message
