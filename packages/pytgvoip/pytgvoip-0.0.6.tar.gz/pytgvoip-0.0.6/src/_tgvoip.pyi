# PytgVoIP - Telegram VoIP Library for Python
# Copyright (C) 2019 bakatrouble <https://github.com/bakatrouble>
#
# This file is part of PytgVoIP.
#
# PytgVoIP is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PytgVoIP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PytgVoIP.  If not, see <http://www.gnu.org/licenses/>.


from enum import Enum
from typing import Optional, List


class NetType(Enum):
    UNKNOWN = ...
    GPRS = ...
    EDGE = ...
    NET_3G = ...
    HSPA = ...
    LTE = ...
    WIFI = ...
    ETHERNET = ...
    OTHER_HIGH_SPEED = ...
    OTHER_LOW_SPEED = ...
    DIALUP = ...
    OTHER_MOBILE = ...


class CallState(Enum):
    WAIT_INIT = ...
    WAIT_INIT_ACK = ...
    ESTABLISHED = ...
    FAILED = ...
    RECONNECTING = ...


class DataSaving(Enum):
    NEVER = ...
    MOBILE = ...
    ALWAYS = ...


class CallError(Enum):
    UNKNOWN = ...
    INCOMPATIBLE = ...
    TIMEOUT = ...
    AUDIO_IO = ...
    PROXY = ...


class Stats:
    bytes_sent_wifi = ...
    bytes_sent_mobile = ...
    bytes_recvd_wifi = ...
    bytes_recvd_mobile = ...


# class AudioInputDevice:
#     _id = ...
#     display_name = ...


# class AudioOutputDevice:
#     _id = ...
#     display_name = ...


class Endpoint:
    _id: int = ...
    ip: str = ...
    ipv6: str = ...
    port: int = ...
    peer_tag: bytes = ...

    def __init__(self, _id: int, ip: str, ipv6: str, port: int, peer_tag: bytes): ...


class VoIPController:
    LIBTGVOIP_VERSION: str = ...
    CONNECTION_MAX_LAYER: int = ...

    def __init__(self, persistent_state_file: str = ''): ...
    def _init(self) -> None: ...
    def start(self) -> None: ...
    def connect(self) -> None: ...
    def set_proxy(self, address: str, port: int, username: str, password: str) -> None: ...
    def set_encryption_key(self, key: bytes, is_outgoing: bool) -> None: ...
    def set_remote_endpoints(self, endpoints: list, allow_p2p: bool, tcp: bool, connection_max_layer: int) -> None: ...
    def get_debug_string(self) -> str: ...
    def set_network_type(self, _type: NetType) -> None: ...
    def set_mic_mute(self, mute: bool) -> None: ...
    def set_config(self, recv_timeout: float, init_timeout: float, data_saving_mode: DataSaving, enable_aec: bool,
                   enable_ns: bool, enable_agc: bool, log_file_path: str, status_dump_path: str,
                   log_packet_stats: bool) -> None: ...
    def debug_ctl(self, request: int, param: int) -> None: ...
    def get_preferred_relay_id(self) -> int: ...
    def get_last_error(self) -> CallError: ...
    def get_stats(self) -> Stats: ...
    def get_debug_log(self) -> str: ...
    def set_audio_output_gain_control_enabled(self, enabled: bool) -> None: ...
    def set_echo_cancellation_strength(self, strength: int) -> None: ...
    def get_peer_capabilities(self) -> int: ...
    def need_rate(self) -> bool: ...

    # @staticmethod
    # def enumerate_audio_inputs() -> List[AudioInputDevice]: ...
    #
    # @staticmethod
    # def enumerate_audio_outputs() -> List[AudioOutputDevice]: ...
    #
    # def set_current_audio_input(self, _id: str) -> None: ...
    # def set_current_audio_output(self, _id: str) -> None: ...
    # def get_current_audio_input_id(self) -> str: ...
    # def get_current_audio_output_id(self) -> str: ...

    def _handle_state_change(self, state: CallState) -> None:
        raise NotImplementedError()

    def _handle_signal_bars_change(self, count: int) -> None:
        raise NotImplementedError()

    def _send_audio_frame_impl(self, length: int) -> bytes: ...
    def _recv_audio_frame_impl(self, frame: bytes) -> None: ...


class VoIPServerConfig:
    @staticmethod
    def set_config(json_string: str): ...


__version__: str = ...
