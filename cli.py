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
from commands import CliCommands


class CLI:
    def __init__(self, ble_sstream, dataset):
        self._commands = CliCommands(ble_sstream, dataset)
        readline.set_completer(self.completer)
        readline.parse_and_bind('tab: complete')

    def completer(self, text, state):
        options = [c for c in self._commands.command_map.keys() if c.startswith(text)]
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

        if command not in self._commands.command_map:
            raise Exception('Invalid command: {}'.format(command))

        return await self._commands.command_map[command](args)
