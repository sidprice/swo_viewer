import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from itm_parser.itm_parser import ITMParser, Protocol_State


@pytest.fixture
def itm_parser():
    return ITMParser()


def test_initializer(itm_parser):
    assert itm_parser is not None
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE


#
# Test the ITM state machine transitions into sync state
# from the IDLE state with 0x00 input
#
def test_state_syncing(itm_parser):
    itm_parser.parse(0)
    assert itm_parser.get_state() == Protocol_State.ITM_SYNCING


#
# Test the ITM state machine transitions into timestamp state
# from the IDLE state with 0x00 input.
#
# TODO: This is a very basic test, the full implementation of the timestamp
# packet handler is not implemented yet.
#
def test_state_timestamp(itm_parser):
    itm_parser.parse(0xC0)
    assert itm_parser.get_state() == Protocol_State.ITM_TS


#
# Test the ITM state machine transitions into SWIT state from
# the IDLE state with 0x01 input.
#
# TODO: This is a very basic test, the full implementation of the SWIT
# packet handler is not implemented yet.
#
def test_state_swit(itm_parser):
    itm_parser.parse(0x01)
    assert itm_parser.get_state() == Protocol_State.ITM_SWIT


#
# Test the ITM state machine transitions into the overflow state from IDLE
#
def test_state_overflow(itm_parser):
    itm_parser.parse(0x38)
    assert itm_parser.get_state() == Protocol_State.ITM_OVERFLOW
    #
    # Test recovery from overflow state
    #
    itm_parser.parse(0x00)
    assert itm_parser.get_state() == Protocol_State.ITM_SYNCING
    itm_parser.parse(0x00)
    itm_parser.parse(0x00)
    itm_parser.parse(0x00)
    itm_parser.parse(0x80)
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE


#
# Send the passed packet to the parser
#
def _send_packet(packet, parser):
    for data in packet:
        parser.parse(data)


#
# Test reception of multiple SWIT packets
#
def test_multiple_swit_packets(itm_parser):
    packet_1 = [0x01, 0x41]
    packet_2 = [0x01, 0x42]
    packet_3 = [0x01, 0x43]
    packet_4 = [0x01, 0x44]

    _send_packet(packet_1, itm_parser)
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE
    _send_packet(packet_2, itm_parser)
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE
    _send_packet(packet_3, itm_parser)
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE
    _send_packet(packet_4, itm_parser)
    assert itm_parser.get_state() == Protocol_State.ITM_IDLE
