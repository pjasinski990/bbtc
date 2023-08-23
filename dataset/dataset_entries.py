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
from typing import List
from abc import ABC, abstractmethod

from tlv.dataset_tlv import MeshcopTlvType
from tlv.tlv import TLV


class DatasetEntry(ABC):
    def __init__(self, type: MeshcopTlvType):
        self.type = type
        self.used = False
        self._length = None
        self._maxlen = None

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
        self._length = 8  # spec defined
        self._seconds = 0
        self._ubit = 0
        self._ticks = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        (value,) = struct.unpack('>Q', tlv.value)
        self._ubit = value & 0x1
        self._ticks = (value >> 1) & 0x7FFF
        self._seconds = (value >> 16) & 0xFFFF

    def to_tlv(self):
        value = (self._seconds << 16) | (self._ticks << 1) | self._ubit
        tlv = struct.pack('>BBQ', self.type.value, self._length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class PendingTimestamp(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PENDINGTIMESTAMP)
        self._length = 8  # spec defined
        self._seconds = 0
        self._ubit = 0
        self._ticks = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        (value,) = struct.unpack('>Q', tlv.value)
        self._ubit = value & 0x1
        self._ticks = (value >> 1) & 0x7FFF
        self._seconds = (value >> 16) & 0xFFFF

    def to_tlv(self):
        value = (self._seconds << 16) | (self._ticks << 1) | self._ubit
        tlv = struct.pack('>BBQ', self.type.value, self._length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class NetworkKey(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKKEY)
        self._length = 16  # spec defined
        self._data = ''

    def set(self, args: List[str]):
        nk = args[0]
        if not nk:
            raise ValueError('Invalid networkkey format')
        if len(nk) != self._length * 2:  # need length * 2 hex characters
            raise ValueError('Invalid length of networkkey')
        self._data = nk

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.hex()

    def to_tlv(self):
        if len(self._data) != self._length * 2:  # need length * 2 hex characters
            raise ValueError('Invalid length of networkkey')
        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class NetworkName(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKNAME)
        self._max_length = 16
        self._data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.decode('utf-8')

    def to_tlv(self):
        length_value = len(self._data)
        value = self._data.encode('utf-8')
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ExtPanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.EXTPANID)
        self._length = 8  # spec defined
        self._data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.hex()

    def to_tlv(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of ExtPanID')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class MeshLocalPrefix(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.MESHLOCALPREFIX)
        self._length = 8  # spec defined
        self._data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.hex()

    def to_tlv(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of MeshLocalPrefix')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class DelayTimer(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.DELAYTIMER)
        self._length = 4  # spec defined
        self._time_remaining = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._time_remaining = tlv.value

    def to_tlv(self):
        value = self._time_remaining
        tlv = struct.pack('>BBI', self.type.value, self._length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class PanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PANID)
        self._length = 2  # spec defined
        self._data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.hex()

    def to_tlv(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of PanID')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class Channel(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNEL)
        self._length = 3  # spec defined
        self._channel_page = 0
        self._channel = 0

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        # TODO this needs to be verified
        self._channel = int.from_bytes(tlv.value[1:3], byteorder='big')
        self._channel_page = tlv.value[0]

    def to_tlv(self):
        tlv = struct.pack('>BBB', self.type.value, self._length, self._channel_page)
        tlv += struct.pack('>H', self._channel)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class Pskc(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PSKC)
        self._max_length = 16
        self._data = ''

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._data = tlv.value.hex()

    def to_tlv(self):
        if (
            len(self._data) > self._max_length * 2
        ):  # should not exceed max length*2 hex characters
            raise ValueError('Invalid length of Pskc')

        length_value = len(self._data) // 2
        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class SecurityPolicy(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.SECURITYPOLICY)
        self._length = 4  # spec defined
        self._rotation_time = 0
        self._out_of_band = 0  # O
        self._native = 0  # N
        self._routers_1_2 = 0  # R
        self._external_commissioners = 0  # C
        self._reserved = 0  # B
        self._commercial_commissioning_off = 0  # CCM
        self._autonomous_enrollment_off = 0  # AE
        self._networkkey_provisioning_off = 0  # NP
        self._thread_over_ble = 0  # L
        self._non_ccm_routers_off = 0  # NCR
        self._rsv = 0b111  # Rsv
        self._version_threshold_for_routing = 0  # VR

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        value = int.from_bytes(tlv.value, byteorder='big')

        self._rotation_time = (value >> 16) & 0xFFFF
        self._out_of_band = (value >> 15) & 0x1
        self._native = (value >> 14) & 0x1
        self._routers_1_2 = (value >> 13) & 0x1
        self._external_commissioners = (value >> 12) & 0x1
        self._reserved = (value >> 11) & 0x1
        self._commercial_commissioning_off = (value >> 10) & 0x1
        self._autonomous_enrollment_off = (value >> 9) & 0x1
        self._networkkey_provisioning_off = (value >> 8) & 0x1
        self._thread_over_ble = (value >> 7) & 0x1
        self._non_ccm_routers_off = (value >> 6) & 0x1
        self._rsv = (value >> 3) & 0x7
        self._version_threshold_for_routing = value & 0x7

    def to_tlv(self):
        value = self._rotation_time << 16
        value |= self._out_of_band << 15
        value |= self._native << 14
        value |= self._routers_1_2 << 13
        value |= self._external_commissioners << 12
        value |= self._reserved << 11
        value |= self._commercial_commissioning_off << 10
        value |= self._autonomous_enrollment_off << 9
        value |= self._networkkey_provisioning_off << 8
        value |= self._thread_over_ble << 7
        value |= self._non_ccm_routers_off << 6
        value |= self._rsv << 3
        value |= self._version_threshold_for_routing
        tlv = struct.pack('>BBI', 1, self._length, value)
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ChannelMask(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNELMASK)
        self._entries: List[ChannelMaskEntry] = []

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._entries = []
        for mask_entry_tlv in TLV.parse_tlvs(tlv.value):
            new_entry = ChannelMaskEntry()
            new_entry.set_from_tlv(mask_entry_tlv)
            self._entries.append(new_entry)

    def to_tlv(self):
        tlv_value = b''.join(mask_entry.to_tlv().to_bytes() for mask_entry in self._entries)
        tlv = struct.pack('>BB', self.type.value, len(tlv_value)) + tlv_value
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


class ChannelMaskEntry(DatasetEntry):
    def __init__(self):
        self._channel_page = 0
        self._mask_length = 0
        self._channel_mask: bytes = None

    def set(self, args: List[str]):
        pass

    def set_from_tlv(self, tlv: TLV):
        self._channel_page = tlv.type
        self._mask_length = len(tlv.value)
        self._channel_mask = tlv.value

    def to_tlv(self):
        tlv = struct.pack('>BB', self._channel_page, self._mask_length) + self._channel_mask
        return TLV.from_bytes(tlv)

    def expected_args_explanation() -> str:
        pass


def create_dataset_entry(type: MeshcopTlvType, args = None):
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

# config_instance = create_dataset_entry(MeshcopTlvType.CHANNEL)
# print(type(config_instance))
