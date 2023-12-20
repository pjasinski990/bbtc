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


def get_int_in_range(min_value, max_value):
    while True:
        try:
            user_input = int(input('> '))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print('The value is out of range. Try again.')
        except ValueError:
            print('The value is not an integer. Try again.')
        except KeyboardInterrupt:
            quit_with_reason('Program interrupted by user. Quitting.')


def quit_with_reason(reason):
    print(reason)
    exit(1)


def select_device_by_user_input(tcat_devices):
    if tcat_devices:
        print('Found devices:\n')
        for i, device in enumerate(tcat_devices):
            print(f'{i + 1}: {device.name} - {device.address}')
    else:
        print('\nNo devices found.')
        return None

    print('\nSelect the target number to connect to it.')
    selected = get_int_in_range(1, len(tcat_devices))
    device = tcat_devices[selected - 1]
    print('Selected ', device)

    return device
