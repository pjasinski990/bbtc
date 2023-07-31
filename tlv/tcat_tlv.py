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

from enum import Enum


class TcatTLVType(Enum):
    COMMAND = 0x00
    RESPONSE = 0x01
    ACTIVE_DATASET = 0x10
    APPLICATION = 0x12

    @classmethod
    def from_value(cls, value: int):
        return cls._value2member_map_.get(value)

    def to_bytes(self):
        return bytes([self.value])


class TcatCommand(Enum):
    COMMAND_THREAD_ON = 0x01
    COMMAND_THREAD_OFF = 0x02

    @classmethod
    def from_value(cls, value: int):
        return cls._value2member_map_.get(value)

    def to_bytes(self):
        return bytes([self.value])
