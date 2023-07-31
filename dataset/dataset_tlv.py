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
from abc import ABC, abstractmethod
import struct


class MeshcopTlvType(Enum):
    CHANNEL = 0
    PANID = 1
    EXTPANID = 2
    NETWORKNAME = 3
    PSKC = 4
    NETWORKKEY = 5
    NETWORK_KEY_SEQUENCE = 6
    MESHLOCALPREFIX = 7
    STEERING_DATA = 8
    BORDER_AGENT_RLOC = 9
    COMMISSIONER_ID = 10
    COMM_SESSION_ID = 11
    SECURITYPOLICY = 12
    GET = 13
    ACTIVETIMESTAMP = 14
    COMMISSIONER_UDP_PORT = 15
    STATE = 16
    JOINER_DTLS = 17
    JOINER_UDP_PORT = 18
    JOINER_IID = 19
    JOINER_RLOC = 20
    JOINER_ROUTER_KEK = 21
    PROVISIONING_URL = 32
    VENDOR_NAME_TLV = 33
    VENDOR_MODEL_TLV = 34
    VENDOR_SW_VERSION_TLV = 35
    VENDOR_DATA_TLV = 36
    VENDOR_STACK_VERSION_TLV = 37
    UDP_ENCAPSULATION_TLV = 48
    IPV6_ADDRESS_TLV = 49
    PENDINGTIMESTAMP = 51
    DELAYTIMER = 52
    CHANNELMASK = 53
    COUNT = 54
    PERIOD = 55
    SCAN_DURATION = 56
    ENERGY_LIST = 57
    DISCOVERYREQUEST = 128
    DISCOVERYRESPONSE = 129
    JOINERADVERTISEMENT = 241

    @classmethod
    def from_value(cls, value: int):
        return cls._value2member_map_.get(value)

    def to_bytes(self):
        return bytes([self.value])


class DatasetEntry(ABC):
    def __init__(self, type: MeshcopTlvType):
        self.type = type
        self.used = False
        self._length = 0

    @abstractmethod
    def to_tlv_bytes(self):
        pass

    @abstractmethod
    def set(self, args):
        pass


class ActiveTimestamp(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.ACTIVETIMESTAMP)
        self._length = 8  # spec defined
        self._seconds = 0
        self._ubit = 0
        self._ticks = 0

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        value = (self._seconds << 16) | (self._ticks << 1) | self._ubit
        tlv = struct.pack('>BBQ', self.type.value, self._length, value)
        return tlv


class PendingTimestamp(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PENDINGTIMESTAMP)
        self._length = 8  # spec defined
        self._seconds = 0
        self._ubit = 0
        self._ticks = 0

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        value = (self._seconds << 16) | (self._ticks << 1) | self._ubit
        tlv = struct.pack('>BBQ', self.type.value, self._length, value)
        return tlv


class NetworkKey(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKKEY)
        self._length = 16  # spec defined
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of networkkey')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return tlv


class NetworkName(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.NETWORKNAME)
        self._max_length = 16
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        length_value = len(self._data)
        value = self._data.encode('utf-8')
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return tlv


class ExtPanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.EXTPANID)
        self._length = 8  # spec defined
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of ExtPanID')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return tlv


class MeshLocalPrefix(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.MESHLOCALPREFIX)
        self._length = 8  # spec defined
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of MeshLocalPrefix')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return tlv


class DelayTimer(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.DELAYTIMER)
        self._length = 4  # spec defined
        self._time_remaining = 0

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        value = self._time_remaining
        tlv = struct.pack('>BBI', self.type.value, self._length, value)
        return tlv


class PanID(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PANID)
        self._length = 2  # spec defined
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        if len(self._data) != self._length * 2:  # need length*2 hex characters
            raise ValueError('Invalid length of PanID')

        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, self._length) + value
        return tlv


class Channel(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNEL)
        self._length = 3  # spec defined
        self._channel_page = 0
        self._channel = 0

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        tlv = struct.pack('>BBB', self.type.value, self._length, self._channel_page)
        tlv += struct.pack('>H', self._channel)
        return tlv


class Pskc(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.PSKC)
        self._max_length = 16
        self._data = ''

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        if (
            len(self._data) > self._max_length * 2
        ):  # should not exceed max length*2 hex characters
            raise ValueError('Invalid length of Pskc')

        length_value = len(self._data) // 2
        value = bytes.fromhex(self._data)
        tlv = struct.pack('>BB', self.type.value, length_value) + value
        return tlv


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

    def set(self, args):
        pass

    def to_tlv_bytes(self):
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
        return tlv


class ChannelMask(DatasetEntry):
    def __init__(self):
        super().__init__(MeshcopTlvType.CHANNELMASK)
        self._entries = []

    def set(self, args):
        pass

    def to_tlv_bytes(self):
        tlv = struct.pack('>BB', self.type.value, len(self._entries))
        for entry in self._entries:
            tlv += entry.to_tlv_bytes()
        return tlv


class ChannelMaskEntry:
    def __init__(self):
        self._channel_page = 0
        self._mask_length = 0
        self._channel_mask = []

    def to_tlv_bytes(self):
        tlv = struct.pack('>BB', self._channel_page, self._mask_length)
        for mask in self._channel_mask:
            tlv += struct.pack('>B', mask)
        return tlv
