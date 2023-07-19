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

from bleak import BLEDevice, BleakScanner, AdvertisementData

async def find_first_by_service_uuid(service_uuid):
    match_uuid = lambda dev, adv_data: service_uuid.lower() in adv_data.service_uuids
    device = await BleakScanner.find_device_by_filter(match_uuid)
    return device


async def find_first_by_name(name):
    match_name = lambda dev, adv_data: name == dev.name
    device = await BleakScanner.find_device_by_filter(match_name)
    return device


async def find_first_by_mac(mac):
    match_mac = lambda dev, adv_data: mac.upper() == dev.address
    device = await BleakScanner.find_device_by_filter(match_mac)
    return device


def test():
    # scanner = BleakScanner()
    # devices = await scanner.discover()
    # devices_matching = []
    # for device in devices:
    #     if args.mac and device.address.lower() == args.mac.lower():
    #         devices_matching.append(device)
    #     elif args.name and device.name == args.name:
    #         devices_matching.append(device)
    #     elif args.uuid and args.uuid.lower() in [service.uuid.lower() for service in device.get_services()]:
    #         devices_matching.append(device)

    # print('select the target:')
    # for i, device in enumerate(devices_matching):
    #     print(f'{i+1}: {device.name} - {device.address}')
    # selected = get_int_in_range(1, len(devices_matching))
    # device = devices_matching[selected-1]
    # print('selected ', device)
    # print(type(device))
    pass
