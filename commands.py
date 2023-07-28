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

from dataset import dataset
from tcat_tlv import TcatTLV


class CliCommands:
    def __init__(self, ble_sstream, dataset):
        self._ble_sstream = ble_sstream
        self._dataset = dataset
        self.command_map = {
            'help': self.help,
            'commission': self.commission,
            'thread': self.thread_state_update,
            'hello': self.say_hello,
            'dataset': self.dataset,
        }

    async def help(self, args=[]):
        print('Available commands:')
        print('\tcommission - send dataset')
        print('\tthread on - enable thread')
        print('\tthread off - disable thread')
        print('\thello - send "hello world" application data')
        print('\texit - close the connection and exit')
        print('\tdataset - display and manipulate Thread dataset')

    async def commission(self, args=[]):
        print('Commissioning...')
        data = TcatTLV(TcatTLV.Type.ACTIVE_DATASET, dataset.dataset).to_bytes()
        await self._ble_sstream.send(data)
        print('Done')

    async def thread_state_update(self, args=[]):
        if not args[0] or args[0] not in ('on', 'off'):
            print('Incorrect usage. See help for details.')
            return

        tlv_response = None
        if args[0] == 'on':
            print('Enabling Thread')
            data = TcatTLV(
                TcatTLV.Type.COMMAND, TcatTLV.Command.COMMAND_THREAD_ON.to_bytes()
            ).to_bytes()
            response = await self._ble_sstream.send_with_resp(data)
            tlv_response = TcatTLV.from_bytes(response)
        elif args[0] == 'off':
            print('Disabling Thread')
            data = TcatTLV(
                TcatTLV.Type.COMMAND, TcatTLV.Command.COMMAND_THREAD_OFF.to_bytes()
            ).to_bytes()
            response = await self._ble_sstream.send_with_resp(data)
            tlv_response = TcatTLV.from_bytes(response)
        return tlv_response

    async def say_hello(self, args=[]):
        print('Sending hello world')
        data = TcatTLV(TcatTLV.Type.APPLICATION, bytes('hello_world', 'ascii')).to_bytes()
        response = await self._ble_sstream.send_with_resp(data)
        tlv_response = TcatTLV.from_bytes(response)
        return tlv_response

    async def dataset(self, args=[]):
        print('Current dataset:')
        print(self._dataset)
