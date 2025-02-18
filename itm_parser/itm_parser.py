from enum import Enum
from typing import List


#
# Enumerate the ITM protocol states
#
class Protocol_State(Enum):
    ITM_IDLE = 0
    ITM_SYNCING = 1
    ITM_TS = 2
    ITM_SWIT = 3
    ITM_OVERFLOW = 4


class ITMParser:
    #
    # Define the ITM Protocol Packet Types
    #
    class _protocol_packet_types(Enum):
        ITM_Sync_Packet = 0
        ITM_Overflow_Packet = 0x38
        ITM_TS_Packet = 0x80  # TODO - The TRM shows 0xC0, check this out when we have timestamps emitted

    def __init__(self):
        self._state: Protocol_State = Protocol_State.ITM_IDLE
        self._rx_packet: bytearray = bytearray(8)
        self._zero_count: int = 0
        self._current_count: int = 0
        self._target_count: int = 0
        #
        # The ITM Protocol State Register
        #
        self._state = Protocol_State.ITM_IDLE
        #
        # ITM Protocol State Names for Debug
        #
        itm_state_names: List[str] = ["ITM_IDLE", "ITM_SYNCING", "ITM_TS", "ITM_SWIT"]

    def parse(self, data_input: int):
        match self._state:
            case Protocol_State.ITM_IDLE:
                if data_input == self._protocol_packet_types.ITM_Overflow_Packet.value:
                    self._state = Protocol_State.ITM_OVERFLOW

                elif data_input == self._protocol_packet_types.ITM_Sync_Packet.value:
                    self._zero_count += 1
                    self._target_count = 4  # Expecting 4 bytes of sync packet
                    self._current_count = 0
                    self._state = Protocol_State.ITM_SYNCING

                elif not (data_input & 0x0F):  # Timestamp packet?
                    self._rx_packet[0] = data_input
                    self._current_count = 1
                    if not (data_input & 0x80):  # Single Byte Timestamp Packet?
                        pass  # Implement TS Packet Handler
                    else:
                        self._state = Protocol_State.ITM_TS

                elif data_input & 0x0F == 0x04:  # Reserved Packet Type
                    # Ignore this unknown/reserved packet
                    self._state = Protocol_State.ITM_IDLE

                elif ~data_input & 0x04 == 0x04:  # SWIT Packet
                    self._target_count = data_input & 0x03
                    if self._target_count == 3:
                        self._target_count = 4
                    Source_Channel = (data_input & 0xF8) >> 3
                    self._current_count = 0
                    self._state = Protocol_State.ITM_SWIT

            case Protocol_State.ITM_OVERFLOW:
                #
                # Stay in this state until a sync byte is received
                #
                if data_input == self._protocol_packet_types.ITM_Sync_Packet.value:
                    self._zero_count += 1
                    self._target_count = 4  # Expecting 4 bytes of sync packet
                    self._current_count = 0
                    self._state = Protocol_State.ITM_SYNCING

            case Protocol_State.ITM_SWIT:
                self._rx_packet[self._current_count] = data_input
                print(chr(data_input), end="")
                self._current_count += 1
                if self._current_count >= self._target_count:
                    self._state = Protocol_State.ITM_IDLE
                    # Implement SWIT Packet Handler

            case Protocol_State.ITM_TS:
                self._rx_packet[self._current_count] = data_input
                self._current_count += 1
                if not (self._rx_packet[0] & 0x80):
                    pass  # Implement TS Packet Handler
                else:
                    if self._current_count >= 4:
                        self.__state = (
                            Protocol_State.ITM_IDLE
                        )  # Something went wrong, restart state machine to resync

            case Protocol_State.ITM_SYNCING:
                self._zero_count += 1
                if data_input == 0x00 and self._current_count < self._target_count:
                    self._current_count += 1
                else:
                    if data_input == 0x80:
                        self._state = Protocol_State.ITM_IDLE
                    # else:
                    #     self._state = Protocol_State.ITM_IDLE  # Unknown state

            case _:
                print("Unknown ITM State")

    def get_state(self) -> Protocol_State:
        return self._state
