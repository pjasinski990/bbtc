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

from .dataset_types import *

dataset = bytes([
    0x0e, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x12, 0x35,
    0x06, 0x00, 0x04, 0x00, 0x1f, 0xff, 0xe0, 0x02,
    0x08, 0xef, 0x13, 0x98, 0xc2, 0xfd, 0x50, 0x4b,
    0x67, 0x07, 0x08, 0xfd, 0x35, 0x34, 0x41, 0x33,
    0xd1, 0xd7, 0x3e, 0x05, 0x10, 0xfd, 0xa7, 0xc7,
    0x71, 0xa2, 0x72, 0x02, 0xe2, 0x32, 0xec, 0xd0,
    0x4c, 0xf9, 0x34, 0xf4, 0x76, 0x03, 0x0f, 0x4f,
    0x70, 0x65, 0x6e, 0x54, 0x68, 0x72, 0x65, 0x61,
    0x64, 0x2d, 0x63, 0x36, 0x34, 0x65, 0x01, 0x02,
    0xc6, 0x4e, 0x04, 0x10, 0x5e, 0x9b, 0x9b, 0x36,
    0x0f, 0x80, 0xb8, 0x8b, 0xe2, 0x60, 0x3f, 0xb0,
    0x13, 0x5c, 0x8d, 0x65, 0x0c, 0x04, 0x02, 0xa0,
    0xf7, 0xf8])


# dataset = bytearray.fromhex(
#     '0e080000000000010000000300001235\
#      060004001fffe00208ef1398c2fd504b\
#      670708fd35344133d1d73e0510fda7c7\
#      71a27202e232ecd04cf934f476030f4f\
#      70656e5468726561642d633634650102\
#      c64e04105e9b9b360f80b88be2603fb0\
#      135c8d650c0402a0f7f8')

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


    def get_entries(self):
        fields = vars(self).values()
        entries = [field for field in fields if isinstance(field, DatasetEntry)]
        return entries


    def __str__(self) -> str:
        res = ''
        width = 20
        for entry in self.get_entries():
            typelen = len(entry.type.name)
            res += f'{entry.type.name}{" " * (width - typelen)} - {entry}\n'
        res = res[:-1]
        return res


    def to_tlvs_hexstring(self):
        fields = vars(self).values()
        tlvs = [field for field in fields if isinstance(field, DatasetEntry)]
        for tlv in tlvs:
            print(tlv.type)