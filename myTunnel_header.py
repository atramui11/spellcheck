from scapy.all import *
import sys, os
#from scapy.fields import  StrField, ShortField ##IEEEDoubleField #, BitField, ByteField

TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800

class SPCHK(Packet):
    name = "SPCHK"
    fields_desc = [
        ByteField("length", 4),
        StrLenField("word", "", length_from=lambda x:x.length),
        #StrFixedLenField("word","",length),
        ByteField("rsp", 2)
        ]

    def mysummary(self):
        return self.sprintf("pid=%pid%, dst_id=%dst_id%")

#think this is OK
bind_layers(Ether, IP, type=TYPE_IPV4)
bind_layers(IP, TCP)
bind_layers(TCP, SPCHK)

#bind_layers(Ether, SPCHK, type=TYPE_MYTUNNEL)
#bind_layers(SPCHK, IP, pid=TYPE_IPV4)


"""
from scapy.packet import Packet, bind_layers
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP
#layer is subclass of Packet class
class SPCK(Packet):
    name = "SPCK"
    fields_desc = [StrField("word",'aa'), ShortField("rsp",2)] 
"""
