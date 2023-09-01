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

from ble.ble_stream_secure import BleStreamSecure
from tlv.tlv import TLV
from tlv.tcat_tlv import TcatTLVType
from cli.command import Command, CommandResultNone, CommandResultTLV
from dataset.dataset import ThreadDataset


class HelpCommand(Command):
    def get_help_string(self) -> str:
        return 'Display help and return.'

    async def execute_default(self, args, context):
        commands = context['commands']
        for name, command in commands.items():
            print(f'{name}')
            command.print_help(indent=1)
        return CommandResultNone()


class HelloCommand(Command):
    def get_help_string(self) -> str:
        return 'Send round trip "Hello world!" message.'

    async def execute_default(self, args, context):
        bless: BleStreamSecure = context['ble_sstream']
        print('Sending hello world...')
        data = TLV(
            TcatTLVType.APPLICATION.value,
            bytes(
                'Hello world!',
                'ascii')).to_bytes()
        response = await bless.send_with_resp(data)
        if not response:
            return
        tlv_response = TLV.from_bytes(response)
        return CommandResultTLV(tlv_response)


class CommissionCommand(Command):
    def get_help_string(self) -> str:
        return 'Update the connected device with current dataset.'

    async def execute_default(self, args, context):
        bless: BleStreamSecure = context['ble_sstream']
        dataset: ThreadDataset = context['dataset']

        print('Commissioning...')
        dataset_bytes = dataset.to_bytes()
        data = TLV(TcatTLVType.ACTIVE_DATASET.value, dataset_bytes).to_bytes()
        response = await bless.send_with_resp(data)
        if not response:
            return
        tlv_response = TLV.from_bytes(response)
        return CommandResultTLV(tlv_response)


class ThreadStartCommand(Command):
    def get_help_string(self) -> str:
        return 'Enable thread interface.'

    async def execute_default(self, args, context):
        bless: BleStreamSecure = context['ble_sstream']

        print('Enabling Thread...')
        data = TLV(
            TcatTLVType.THREAD_START.value, bytes()
        ).to_bytes()
        response = await bless.send_with_resp(data)
        if not response:
            return
        tlv_response = TLV.from_bytes(response)
        return CommandResultTLV(tlv_response)


class ThreadStopCommand(Command):
    def get_help_string(self) -> str:
        return 'Disable thread interface.'

    async def execute_default(self, args, context):
        bless: BleStreamSecure = context['ble_sstream']
        print('Disabling Thread...')
        data = TLV(
            TcatTLVType.THREAD_STOP.value, bytes()
        ).to_bytes()
        response = await bless.send_with_resp(data)
        if not response:
            return
        tlv_response = TLV.from_bytes(response)
        return CommandResultTLV(tlv_response)


class ThreadStateCommand(Command):
    def __init__(self):
        self._subcommands = {
            'start': ThreadStartCommand(),
            'stop': ThreadStopCommand()
        }

    def get_help_string(self) -> str:
        return 'Manipulate state of the Thread interface of the connected device.'

    async def execute_default(self, args, context):
        print('Invalid usage. Provide a subcommand.')
        return CommandResultNone()
