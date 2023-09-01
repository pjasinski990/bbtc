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

import readline
import shlex
from cli.base_commands import (
    HelpCommand,
    HelloCommand,
    CommissionCommand,
    ThreadStateCommand
)
from cli.dataset_commands import (
    DatasetCommand
)


class CLI:
    def __init__(self, ble_sstream, dataset):
        self._commands = {
            'help': HelpCommand(),
            'hello': HelloCommand(),
            'commission': CommissionCommand(),
            'thread': ThreadStateCommand(),
            'dataset': DatasetCommand()
        }
        self._context = {
            'ble_sstream': ble_sstream,
            'dataset': dataset,
            'commands': self._commands
        }
        readline.set_completer(self.completer)
        readline.parse_and_bind('tab: complete')

    def completer(self, text, state):
        command_pool = self._commands.keys()
        full_line = readline.get_line_buffer().lstrip()
        words = full_line.split()

        should_suggest_subcommands = len(words) > 1 or (
            len(words) == 1 and full_line[-1].isspace())
        if should_suggest_subcommands:
            if words[0] not in self._commands.keys():
                return None

            current_command = self._commands[words[0]]
            if full_line[-1].isspace():
                subcommands = words[1:]
            else:
                subcommands = words[1:-1]
            for nextarg in subcommands:
                if nextarg in current_command._subcommands.keys():
                    current_command = current_command._subcommands[nextarg]
                else:
                    return None

            if len(current_command._subcommands) == 0:
                return None

            command_pool = current_command._subcommands.keys()

        options = [c for c in command_pool if c.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    async def evaluate_input(self, user_input):
        # do not parse empty commands
        if not user_input.strip():
            return

        command_parts = shlex.split(user_input)
        command = command_parts[0]
        args = command_parts[1:]

        if command not in self._commands.keys():
            raise Exception('Invalid command: {}'.format(command))

        return await self._commands[command].execute(args, self._context)
