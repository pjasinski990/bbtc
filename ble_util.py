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
