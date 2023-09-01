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

from cli.command import Command, CommandResultNone
from dataset.dataset import ThreadDataset, initial_dataset
from tlv.dataset_tlv import MeshcopTlvType


def handle_dataset_entry_command(type: MeshcopTlvType, args, context):
    ds: ThreadDataset = context['dataset']
    if len(args) == 0:
        ds.get_entry(type).print_content()
        return CommandResultNone()

    ds.set_entry(type, args)
    print('Done.')
    return CommandResultNone()


class DatasetHelpCommand(Command):
    def get_help_string(self) -> str:
        return 'Display help message and return.'

    async def execute_default(self, args, context):
        indent_width = 4
        indentation = ' ' * indent_width
        commands: ThreadDataset = context['commands']
        ds_command: Command = commands['dataset']
        print(ds_command.get_help_string())
        print('Subcommands:')
        for name, subcommand in ds_command._subcommands.items():
            print(f'{indentation}{name}')
            print(f'{indentation}{" " * indent_width}{subcommand.get_help_string()}')
        return CommandResultNone()


class PrintDatasetHexCommand(Command):
    def get_help_string(self) -> str:
        return 'Print current dataset as a hexadecimal string.'

    async def execute_default(self, args, context):
        ds: ThreadDataset = context['dataset']
        print(ds.to_bytes().hex())
        return CommandResultNone()


class ReloadDatasetCommand(Command):
    def get_help_string(self) -> str:
        return 'Reset dataset to the initial value.'

    async def execute_default(self, args, context):
        context['dataset'].set_from_bytes(initial_dataset)
        return CommandResultNone()


class ActiveTimestampCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set ActiveTimestamp seconds. Arguments: [seconds (int)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.ACTIVETIMESTAMP, args, context)


class PendingTimestampCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set PendingTimestamp seconds. Arguments: [seconds (int)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(
            MeshcopTlvType.PENDINGTIMESTAMP, args, context)


class NetworkKeyCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set NetworkKey. Arguments: [nk (hexstring, len=32)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.NETWORKKEY, args, context)


class NetworkNameCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set NetworkName. Arguments: [nn (string, maxlen=16)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.NETWORKNAME, args, context)


class ExtPanIDCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set ExtPanID. Arguments: [extpanid (hexstring, len=16)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.EXTPANID, args, context)


class MeshLocalPrefixCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set MeshLocalPrefix. Arguments: [mlp (hexstring, len=16)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.MESHLOCALPREFIX, args, context)


class DelayTimerCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set DelayTimer delay. Arguments: [delay (int)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.DELAYTIMER, args, context)


class PanIDCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set PanID. Arguments: [panid (hexstring, len=4)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.PANID, args, context)


class ChannelCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set Channel. Arguments: [channel (int)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.CHANNEL, args, context)


class ChannelMaskCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set ChannelMask. Arguments: [mask (hexstring)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.CHANNELMASK, args, context)


class PskcCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set Pskc. Arguments: [pskc (hexstring, maxlen=32)]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.PSKC, args, context)


class SecurityPolicyCommand(Command):
    def get_help_string(self) -> str:
        return 'View and set SecurityPolicy. Arguments: '\
               '[<rotation_time (int)> [flags (string)] [version_threshold (int)]]'

    async def execute_default(self, args, context):
        return handle_dataset_entry_command(MeshcopTlvType.SECURITYPOLICY, args, context)


class DatasetCommand(Command):
    def __init__(self):
        self._subcommands = {
            'help': DatasetHelpCommand(),
            'hex': PrintDatasetHexCommand(),
            'reload': ReloadDatasetCommand(),
            'activetimestamp': ActiveTimestampCommand(),
            'pendingtimestamp': PendingTimestampCommand(),
            'networkkey': NetworkKeyCommand(),
            'networkname': NetworkNameCommand(),
            'extpanid': ExtPanIDCommand(),
            'meshlocalprefix': MeshLocalPrefixCommand(),
            'delay': DelayTimerCommand(),
            'panid': PanIDCommand(),
            'channel': ChannelCommand(),
            'channelmask': ChannelMaskCommand(),
            'pskc': PskcCommand(),
            'securitypolicy': SecurityPolicyCommand()
        }

    def get_help_string(self) -> str:
        return 'View and manipulate current dataset. ' \
            'Call without parameters to show current dataset.'

    async def execute_default(self, args, context):
        ds: ThreadDataset = context['dataset']
        ds.print_content()
        return CommandResultNone()
