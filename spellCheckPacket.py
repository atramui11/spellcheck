from scapy.fields import IEEEDoubleField #, BitField, ByteField
from scapy.packet import Packet #, bind_layers
#from scapy.layers.inet import IP
#from scapy.layers.l2 import Ether, ARP


#layer is subclass of Packet class
class spellCheckPacket(Packet):
    name = "spellCheckPacket"
    fields_desc = [ IEEEDoubleField("spellCheckWord", None)]

                    
#not sure if needed
#bind_layers(IP, spellCheckPacket,  frag=0, proto=0x61)
#bind_layers(spellCheckPacket, Ether)