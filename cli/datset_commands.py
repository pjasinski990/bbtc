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

from cli.command import Command
from dataset.dataset import ThreadDataset
from tlv.dataset_tlv import MeshcopTlvType


def handle_dataset_entry_command(type: MeshcopTlvType, args, context):
    ds: ThreadDataset = context['dataset']
    if len(args) == 0:
        ds.get_entry(type).print_content()
        return

    ds.set_entry(type, args)
    print('Done.')


class ActiveTimestampCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set ActiveTimestamp seconds.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.ACTIVETIMESTAMP, args, context)


class PendingTimestampCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set PendingTimestamp seconds.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.PENDINGTIMESTAMP, args, context)


class NetworkKeyCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set NetworkKey.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.NETWORKKEY, args, context)


class NetworkNameCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set NetworkName.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.NETWORKNAME, args, context)


class ExtPanIDCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set ExtPanID.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.EXTPANID, args, context)


class MeshLocalPrefixCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set MeshLocalPrefix.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.MESHLOCALPREFIX, args, context)


class DelayTimerCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set DelayTimer delay.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.DELAYTIMER, args, context)


class PanIDCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set PanID.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.PANID, args, context)


class ChannelCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set Channel.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.CHANNEL, args, context)


class PskcCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set Pskc.'

    async def execute_default(self, args, context):
        handle_dataset_entry_command(MeshcopTlvType.PSKC, args, context)


class DatasetCommand(Command):
    def __init__(self):
        self._subcommands = {
            'activetimestamp': ActiveTimestampCommand(),
            'pendingtimestamp': PendingTimestampCommand(),
            'networkkey': NetworkKeyCommand(),
            'networkname': NetworkNameCommand(),
            'extpanid': ExtPanIDCommand(),
            'meshlocalprefix': MeshLocalPrefixCommand(),
            'delay': DelayTimerCommand(),
            'panid': PanIDCommand(),
            'channel': ChannelCommand(),
            'pskc': PskcCommand()
        }

    def get_help_string(self) -> str:
        return 'View and manipulate current dataset. ' \
            'Call without parameters to show current dataset.'

    async def execute_default(self, args, context):
        ds: ThreadDataset = context['dataset']
        ds.print_content()
