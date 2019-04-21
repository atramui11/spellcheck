from scapy.all import *
import sys, os
#from scapy.fields import  StrField, ShortField ##IEEEDoubleField #, BitField, ByteField

TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800

class MyTunnel(Packet):
    name = "MyTunnel"
    #fields_desc = [StrField("word",'aa'), ShortField("rsp",2)]
    fields_desc = [
        ShortField("pid", 0),
        ShortField("rsp", 2),
        ShortField("dst_id", 0)
        ,X3BytesField("wordp1",None)
        ,X3BytesField("wordp2",None)
    ]
    def mysummary(self):
        return self.sprintf("pid=%pid%, dst_id=%dst_id%")


bind_layers(Ether, MyTunnel, type=TYPE_MYTUNNEL)
bind_layers(MyTunnel, IP, pid=TYPE_IPV4)


"""
from scapy.packet import Packet, bind_layers
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP
#layer is subclass of Packet class
class SPCK(Packet):
    name = "SPCK"
    fields_desc = [StrField("word",'aa'), ShortField("rsp",2)] 
"""
