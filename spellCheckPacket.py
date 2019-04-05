from scapy.fields import BitField, ByteField, ShortField
from scapy.packet import Packet, bind_layers
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether, ARP


#child class of Packet
class spellCheckPacket(Packet):
    name = "spellCheckPacket"
    fields_desc = [ ShortField("spellCheckWord", None),
                    ShortField("srcPort", None)]



#not sure which layers to bind here...if any 

#bind_layers(spellCheckPacket, IP, origEtherType=0x0800)
 