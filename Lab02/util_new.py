from scapy.all import Packet
from scapy.all import IntField

class PacketHeader(Packet):
    TYPE_DATA = 1
    TYPE_ACK = 2
    TYPE_END = 3
    TYPE_FILENAME = 4    # new add

    header_len = 12
    name = "PacketHeader"
    fields_desc = [
        IntField("type", 0),
        IntField("seq_num", 0),
        IntField("length", 0),
    ]
