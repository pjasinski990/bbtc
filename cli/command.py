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

    async def execute(self, args, context):
        if len(args) != 0 and args[0] in self._subcommands.keys():
            return await self.execute_subcommand(args, context)

        return await self.execute_default(args, context)

    async def execute_subcommand(self, args, context):
        return await self._subcommands[args[0]].execute(args[1:], context)

    @abstractmethod
    async def execute_default(self, args, context):
        pass

    @abstractmethod
    def get_help_string(self) -> str:
        pass

    def print_help(self, indent=0):
        indent_width = 4
        indentation = ' ' * indent_width * indent
        print(f'{indentation}{self.get_help_string()}')

        if 'help' in self._subcommands.keys():
            print(f'{indentation}"help" command available.')
        elif len(self._subcommands) != 0:
            print(f'{indentation}Subcommands:')
            for name, sc in self._subcommands.items():
                print(f'{indentation}{" " * indent_width}{name}\t- ', end='')
                sc.print_help()


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
