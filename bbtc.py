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
import argparse
from os import path
import logging

from ble_stream import BleStream
from ble_stream_secure import BleStreamSecure
import ble_scanner
from cli import CLI

BBTC_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
BBTC_TX_CHAR_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
BBTC_RX_CHAR_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'


async def main():
    logging.basicConfig(level=logging.ERROR)

    parser = argparse.ArgumentParser(description='Device parameters')
    parser.add_argument('--debug', help='Enable debug logs', action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--mac', type=str, help='Device MAC address', action='store')
    group.add_argument('--name', type=str, help='Device name', action='store')
    group.add_argument('--uuid', type=str, help='Target service UUID', action='store')
    group.add_argument('--scan', help='Scan all available devices', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('ble_stream').setLevel(logging.DEBUG)
        logging.getLogger('ble_stream_secure').setLevel(logging.DEBUG)

    device = await get_device_by_args(args)
    if device is None:
        print('Device not found')
        exit(1)

    print(f'Connecting to {device}...')
    async with await BleStream.create(device.address, BBTC_SERVICE_UUID, BBTC_TX_CHAR_UUID, BBTC_RX_CHAR_UUID) \
            as ble_stream:
        ble_sstream = BleStreamSecure(ble_stream)
        ble_sstream.load_cert(
            certfile=path.join('auth', 'certificate.pem'),
            keyfile=path.join('auth', 'privatekey.pem'),
            cafile=path.join('auth', 'ca_certificate.pem')
            )

        print('Setting up secure channel...')
        await ble_sstream.do_handshake(hostname='DeviceType')
        print('Done')

        cli = CLI(ble_sstream)
        loop = asyncio.get_running_loop()
        print('Enter \'help\' to see available commands')
        while True:
            user_input = await loop.run_in_executor(None, lambda: input('> '))
            if user_input.lower() == 'exit':
                print('Disconnecting...')
                break
            try:
                result = await cli.evaluate_input(user_input)
                if result:
                    print('Result:', result)
            except Exception as e:
                print(e)


async def get_device_by_args(args):
    device = None
    if args.mac:
        device = await ble_scanner.find_first_by_mac(args.mac)
    elif args.name:
        device = await ble_scanner.find_first_by_name(args.name)
    elif args.uuid:
        device = await ble_scanner.find_first_by_service_uuid(args.uuid)
    elif args.scan:
        tcat_devices = await ble_scanner.scan_tcat_devices()
        print('Select the target:')
        for i, device in enumerate(tcat_devices):
            print(f'{i+1}: {device.name} - {device.address}')
        selected = get_int_in_range(1, len(tcat_devices))
        device = tcat_devices[selected-1]
        print('Selected ', device)
    return device


def get_int_in_range(min_value, max_value):
    while True:
        try:
            user_input = int(input())
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print(f'The value is out of range. Try again.')
        except ValueError:
            print(f'The value is not an integer. Try again.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        pass  # device disconnected
