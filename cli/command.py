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

from tlv.tlv import TLV

from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self._subcommands = {}

    @abstractmethod
    async def execute(self, args, context):
        pass

    @abstractmethod
    def get_help_string(self) -> str:
        pass

    async def execute_subcommand(self, args, context):
        if len(args) == 0 or args[0] not in self._subcommands.keys():
            print('Incorrect subcommand. Usage: ')
            print(f'\t{self.print_help(indent=1)}')
            return

        return await self._subcommands[args[0]].execute(args[1:], context)

    def print_help(self, indent=0):
        indentation = ' ' * 4 * indent
        print(f'{indentation}{self.get_help_string()}')
        if len(self._subcommands) != 0:
            print(f'{indentation}subcommands:')
            for name, sc in self._subcommands.items():
                print(f'{indentation}    {name}:')
                sc.print_help(indent=indent + 2)


class CommandResult(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def pretty_print(self):
        pass


class CommandResultTLV(CommandResult):
    def pretty_print(self):
        value: TLV = self.value
        print(value)


class CommandResultNone(CommandResult):
    def pretty_print(self):
        pass


class CommandResultString(CommandResult):
    def pretty_print(self):
        value: str = self.value
        print(value)
