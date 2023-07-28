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

from bleak import BleakScanner

BBTC_SERVICE_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'


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


async def scan_tcat_devices():
    scanner = BleakScanner()
    tcat_devices = []
    devices_dict = await scanner.discover(return_adv=True)
    for _, (device, adv_data) in devices_dict.items():
        if BBTC_SERVICE_UUID.lower() in adv_data.service_uuids:
            tcat_devices.append(device)
    return tcat_devices
