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

import struct
import inspect
from typing import List
from abc import ABC, abstractmethod

from tlv.dataset_tlv import MeshcopTlvType
from tlv.tlv import TLV


class DatasetEntry(ABC):
    def __init__(self, type: MeshcopTlvType):
        self.type = type
        self.used = False
        self.length = None
        self.maxlen = None

    def print_content(self, indent: int = 0, excluded_fields: List[str] = []):
        excluded_fields += ['length', 'maxlen', 'used', 'type']
        indentation = " " * 4 * indent
        for attr_name in dir(self):
            if not attr_name.startswith('_') and attr_name not in excluded_fields:
                value = getattr(self, attr_name)
                if not inspect.ismethod(value):
                    print(f'{indentation}{attr_name}: {value}')

    @abstractmethod
    def to_tlv(self) -> TLV:
        pass

    @abstractmethod
    def set_from_tlv(self, tlv: TLV):
        pass

    @abstractmethod
    def set(self, args: List[str]):
        pass

    @abstractmethod
    def expected_args_explanation() -> str:
        pass


class ActiveTimestamp(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.ACTIVETIMESTAMP)
        self.length = 8  # spec defined
        self.seconds = 0
        self.ubit = 0
        self.ticks = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        (value,) = struct.unpack('>Q', tlv.value)
        self.ubit = value & 0x1
        self.ticks = (value >> 1) & 0x7FFF
        self.seconds = (value >> 16) & 0xFFFF

    def to_tlv(self):
        value = (self.seconds << 16) | (self.ticks << 1) | self.ubit
        tlv = struct.pack('>BBQ', self.type.value, self.length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class PendingTimestamp(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PENDINGTIMESTAMP)
        self.length = 8  # spec defined
        self.seconds = 0
        self.ubit = 0
        self.ticks = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        (value,) = struct.unpack('>Q', tlv.value)
        self.ubit = value & 0x1
        self.ticks = (value >> 1) & 0x7FFF
        self.seconds = (value >> 16) & 0xFFFF

    def to_tlv(self):
        value = (self.seconds << 16) | (self.ticks << 1) | self.ubit
        tlv = struct.pack('>BBQ', self.type.value, self.length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class NetworkKey(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKKEY)
        self.length = 16  # spec defined
        self.data = ''

    def set(self, args: List[str]):
        nk = args[0]
        if not nk:
            raise ValueError('Invalid networkkey format')
        if len(nk) != self.length * 2:  # need length * 2 hex characters
            raise ValueError('Invalid length of networkkey')
        self.data = nk

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.hex()

    def to_tlv(self):
        if len(self.data) != self.length * 2:  # need length * 2 hex characters
            raise ValueError('Invalid length of networkkey')
        value = bytes.fromhex(self.data)
        tlv = struct.pack('>BB', self.type.value, self.length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class NetworkName(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKNAME)
        self.maxlen = 16
        self.data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.decode('utf-8')

    def to_tlv(self):
        length_value = len(self.data)
        value = self.data.encode('utf-8')
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ExtPanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.EXTPANID)
        self.length = 8  # spec defined
        self.data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.hex()

    def to_tlv(self):
        if len(self.data) != self.length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of ExtPanID')

        value = bytes.fromhex(self.data)
        tlv = struct.pack('>BB', self.type.value, self.length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class MeshLocalPrefix(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.MESHLOCALPREFIX)
        self.length = 8  # spec defined
        self.data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.hex()

    def to_tlv(self):
        if len(self.data) != self.length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of MeshLocalPrefix')

        value = bytes.fromhex(self.data)
        tlv = struct.pack('>BB', self.type.value, self.length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class DelayTimer(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.DELAYTIMER)
        self.length = 4  # spec defined
        self.time_remaining = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.time_remaining = tlv.value

    def to_tlv(self):
        value = self.time_remaining
        tlv = struct.pack('>BBI', self.type.value, self.length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class PanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PANID)
        self.length = 2  # spec defined
        self.data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.hex()

    def to_tlv(self):
        if len(self.data) != self.length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of PanID')

        value = bytes.fromhex(self.data)
        tlv = struct.pack('>BB', self.type.value, self.length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class Channel(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNEL)
        self.length = 3  # spec defined
        self.channel_page = 0
        self.channel = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.channel = int.from_bytes(tlv.value[1:3], byteorder='big')
        self.channel_page = tlv.value[0]

    def to_tlv(self):
        tlv = struct.pack('>BBB', self.type.value, self.length, self.channel_page)
        tlv += struct.pack('>H', self.channel)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class Pskc(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PSKC)
        self.maxlen = 16
        self.data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.data = tlv.value.hex()

    def to_tlv(self):
        if (
            len(self.data) > self.maxlen * 2
        ):  # should not exceed max length*2 hex characters
            raise ValueError('Invalid length of Pskc')

        length_value = len(self.data) // 2
        value = bytes.fromhex(self.data)
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class SecurityPolicy(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.SECURITYPOLICY)
        self.length = 4  # spec defined
        self.rotation_time = 0
        self.out_of_band = 0  # O
        self.native = 0  # N
        self.routers_1_2 = 0  # R
        self.external_commissioners = 0  # C
        self.reserved = 0  # B
        self.commercial_commissioning_off = 0  # CCM
        self.autonomous_enrollment_off = 0  # AE
        self.networkkey_provisioning_off = 0  # NP
        self.thread_over_ble = 0  # L
        self.non_ccm_routers_off = 0  # NCR
        self.rsv = 0b111  # Rsv
        self.version_threshold_for_routing = 0  # VR

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        value = int.from_bytes(tlv.value, byteorder='big')

        self.rotation_time = (value >> 16) & 0xFFFF
        self.out_of_band = (value >> 15) & 0x1
        self.native = (value >> 14) & 0x1
        self.routers_1_2 = (value >> 13) & 0x1
        self.external_commissioners = (value >> 12) & 0x1
        self.reserved = (value >> 11) & 0x1
        self.commercial_commissioning_off = (value >> 10) & 0x1
        self.autonomous_enrollment_off = (value >> 9) & 0x1
        self.networkkey_provisioning_off = (value >> 8) & 0x1
        self.thread_over_ble = (value >> 7) & 0x1
        self.non_ccm_routers_off = (value >> 6) & 0x1
        self.rsv = (value >> 3) & 0x7
        self.version_threshold_for_routing = value & 0x7

    def to_tlv(self):
        value = self.rotation_time << 16
        value |= self.out_of_band << 15
        value |= self.native << 14
        value |= self.routers_1_2 << 13
        value |= self.external_commissioners << 12
        value |= self.reserved << 11
        value |= self.commercial_commissioning_off << 10
        value |= self.autonomous_enrollment_off << 9
        value |= self.networkkey_provisioning_off << 8
        value |= self.thread_over_ble << 7
        value |= self.non_ccm_routers_off << 6
        value |= self.rsv << 3
        value |= self.version_threshold_for_routing
        tlv = struct.pack('>BBI', 1, self.length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ChannelMask(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNELMASK)
        self.entries: List[ChannelMaskEntry] = []

    def set(self, args: List[str]):
        pass

    def print_content(self, indent: int = 0):
        super().print_content(indent=indent, excluded_fields=['entries'])
        indentation = " " * 4 * indent
        for i, entry in enumerate(self.entries):
            print(f'{indentation}ChannelMaskEntry {i}')
            entry.print_content(indent=indent + 1)

    def set_from_tlv(self, tlv: TLV):
        self.entries = []
        for mask_entry_tlv in TLV.parse_tlvs(tlv.value):
            new_entry = ChannelMaskEntry()
            new_entry.set_from_tlv(mask_entry_tlv)
            self.entries.append(new_entry)

    def to_tlv(self):
        tlv_value = b''.join(mask_entry.to_tlv().to_bytes()
                             for mask_entry in self.entries)
        tlv = struct.pack('>BB', self.type.value, len(tlv_value)) + tlv_value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ChannelMaskEntry(DatasetEntry):
    def __init__(self):
        self.channel_page = 0
        self.mask_length = 0
        self.channel_mask: bytes = None

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self.channel_page = tlv.type
        self.mask_length = len(tlv.value)
        self.channel_mask = tlv.value

    def to_tlv(self):
        tlv = struct.pack('>BB', self.channel_page, self.mask_length) + self.channel_mask
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


def create_dataset_entry(type: MeshcopTlvType, args=None):
    entry_classes = {
        MeshcopTlvType.ACTIVETIMESTAMP: ActiveTimestamp,
        MeshcopTlvType.PENDINGTIMESTAMP: PendingTimestamp,
        MeshcopTlvType.NETWORKKEY: NetworkKey,
        MeshcopTlvType.NETWORKNAME: NetworkName,
        MeshcopTlvType.EXTPANID: ExtPanID,
        MeshcopTlvType.MESHLOCALPREFIX: MeshLocalPrefix,
        MeshcopTlvType.DELAYTIMER: DelayTimer,
        MeshcopTlvType.PANID: PanID,
        MeshcopTlvType.CHANNEL: Channel,
        MeshcopTlvType.PSKC: Pskc,
        MeshcopTlvType.SECURITYPOLICY: SecurityPolicy,
        MeshcopTlvType.CHANNELMASK: ChannelMask
    }

    entry_class = entry_classes.get(type)
    if not entry_class:
        raise ValueError(f"Invalid configuration type: {type}")

    res = entry_class()
    if args:
        res.set(args)
    return res
