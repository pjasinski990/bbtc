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

from .dataset_tlv import (
    DatasetEntry,
    ActiveTimestamp,
    PendingTimestamp,
    NetworkKey,
    NetworkName,
    ExtPanID,
    MeshLocalPrefix,
    DelayTimer,
    PanID,
    Channel,
    Pskc,
    SecurityPolicy,
    ChannelMask,
)


dataset = bytes(
    [
        0x0E, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x12, 0x35,
        0x06, 0x00, 0x04, 0x00, 0x1F, 0xFF, 0xE0, 0x02,
        0x08, 0xEF, 0x13, 0x98, 0xC2, 0xFD, 0x50, 0x4B,
        0x67, 0x07, 0x08, 0xFD, 0x35, 0x34, 0x41, 0x33,
        0xD1, 0xD7, 0x3E, 0x05, 0x10, 0xFD, 0xA7, 0xC7,
        0x71, 0xA2, 0x72, 0x02, 0xE2, 0x32, 0xEC, 0xD0,
        0x4C, 0xF9, 0x34, 0xF4, 0x76, 0x03, 0x0F, 0x4F,
        0x70, 0x65, 0x6E, 0x54, 0x68, 0x72, 0x65, 0x61,
        0x64, 0x2D, 0x63, 0x36, 0x34, 0x65, 0x01, 0x02,
        0xC6, 0x4E, 0x04, 0x10, 0x5E, 0x9B, 0x9B, 0x36,
        0x0F, 0x80, 0xB8, 0x8B, 0xE2, 0x60, 0x3F, 0xB0,
        0x13, 0x5C, 0x8D, 0x65, 0x0C, 0x04, 0x02, 0xA0,
        0xF7, 0xF8
    ]
)


class ThreadDataset:
    def __init__(self):
        self.active_timestamp = ActiveTimestamp()
        self.pending_timestamp = PendingTimestamp()
        self.networkkey = NetworkKey()
        self.networkname = NetworkName()
        self.extpanid = ExtPanID()
        self.mlprefix = MeshLocalPrefix()
        self.delay_timer = DelayTimer()
        self.panid = PanID()
        self.channel = Channel()
        self.pskc = Pskc()
        self.secpolicy = SecurityPolicy()
        self.channel_mask = ChannelMask()

    def __str__(self) -> str:
        res = ''
        width = 20
        for entry in self.get_entries():
            typelen = len(entry.type.name)
            res += f'{entry.type.name}{" " * (width - typelen)} - {entry}\n'
        res = res[:-1]
        return res

    def set_from_bytes(bytes):
        pass
        tlvs = TLV.parse_tlvs(bytes)
        for tlv in tlvs:
            pass

    def get_entries(self):
        fields = vars(self).values()
        entries = [field for field in fields if isinstance(field, DatasetEntry)]
        return entries

    def to_tlvs_hexstring(self):
        fields = vars(self).values()
        tlvs = [field for field in fields if isinstance(field, DatasetEntry)]
        for tlv in tlvs:
            print(tlv.type)
