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
from bbtc import BBTC_SERVICE_UUID


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
    devices_dict = await scanner.discover(return_adv=True,
                                          service_uuids=[BBTC_SERVICE_UUID.lower()])
    for _, (device, _) in devices_dict.items():
        tcat_devices.append(device)

    return tcat_devices
