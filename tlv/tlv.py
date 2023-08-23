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

from __future__ import annotations
from typing import List


class TLV():
    def __init__(self, type: int = None, value: bytes = None):
        self.type: int = type
        self.value: bytes = value

    def __str__(self):
        return f'TLV\n\tTYPE:\t0x{self.type:02x}\n\tVALUE:\t{self.value}'

    @staticmethod
    def parse_tlvs(data: bytes) -> List[TLV]:
        res: List[TLV] = []
        while data:
            next_tlv = TLV.from_bytes(data)
            next_tlv_size = len(next_tlv.to_bytes())
            data = data[next_tlv_size:]
            res.append(next_tlv)
        return res

    @staticmethod
    def from_bytes(data: bytes) -> TLV:
        res = TLV()
        res.set_from_bytes(data)
        return res

    def set_from_bytes(self, data: bytes):
        self.type = data[0]
        header_len = 2
        if data[1] == 0xFF:
            header_len = 4
        length = int.from_bytes(data[1:header_len], byteorder='big')
        self.value = data[header_len:header_len + length]

    def to_bytes(self) -> bytes:
        has_long_header = len(self.value) >= 255
        header_len = 4 if has_long_header else 2
        len_bytes = len(self.value).to_bytes(header_len - 1, byteorder='big')
        header = bytes([self.type]) + len_bytes
        return header + self.value