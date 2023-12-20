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

from ble.ble_connection_constants import BBTC_SERVICE_UUID, BBTC_TX_CHAR_UUID, \
    BBTC_RX_CHAR_UUID, SERVER_COMMON_NAME
from ble.ble_stream import BleStream
from ble.ble_stream_secure import BleStreamSecure
from ble import ble_scanner
from cli.cli import CLI
from dataset.dataset import ThreadDataset
from cli.command import CommandResult
from utils import select_device_by_user_input


async def main():
    logging.basicConfig(level=logging.WARNING)

    parser = argparse.ArgumentParser(description='Device parameters')
    parser.add_argument('--debug', help='Enable debug logs', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--mac', type=str, help='Device MAC address', action='store')
    group.add_argument('--name', type=str, help='Device name', action='store')
    group.add_argument('--scan', help='Scan all available devices', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('ble_stream').setLevel(logging.DEBUG)
        logging.getLogger('ble_stream_secure').setLevel(logging.DEBUG)

    device = await get_device_by_args(args)

    ble_sstream = None

    if not (device is None):
        print(f'Connecting to {device}')
        ble_stream = await BleStream.create(
            device.address, BBTC_SERVICE_UUID, BBTC_TX_CHAR_UUID, BBTC_RX_CHAR_UUID
        )
        ble_sstream = BleStreamSecure(ble_stream)
        ble_sstream.load_cert(
            certfile=path.join('auth', 'commissioner_cert.pem'),
            keyfile=path.join('auth', 'commissioner_key.pem'),
            cafile=path.join('auth', 'ca_cert.pem'),
        )

        print('Setting up secure channel...')
        await ble_sstream.do_handshake(hostname=SERVER_COMMON_NAME)
        print('Done')

    ds = ThreadDataset()
    cli = CLI(ds, ble_sstream)
    loop = asyncio.get_running_loop()
    print('Enter \'help\' to see available commands'
          ' or \'exit\' to exit the application.')
    while True:
        user_input = await loop.run_in_executor(None, lambda: input('> '))
        if user_input.lower() == 'exit':
            print('Disconnecting...')
            break
        try:
            result: CommandResult = await cli.evaluate_input(user_input)
            if result:
                result.pretty_print()
        except Exception as e:
            print(e)


async def get_device_by_args(args):
    device = None
    if args.mac:
        device = await ble_scanner.find_first_by_mac(args.mac)
    elif args.name:
        device = await ble_scanner.find_first_by_name(args.name)
    elif args.scan:
        tcat_devices = await ble_scanner.scan_tcat_devices()
        device = select_device_by_user_input(tcat_devices)

    return device

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        pass  # device disconnected
