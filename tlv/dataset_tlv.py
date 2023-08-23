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
