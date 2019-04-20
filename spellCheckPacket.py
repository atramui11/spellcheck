from scapy.fields import  StrField, ShortField ##IEEEDoubleField #, BitField, ByteField
from scapy.packet import Packet, bind_layers
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP


#layer is subclass of Packet class
class SPCK(Packet):
    name = "SPCK"
    fields_desc = [StrField("word",'aa'), ShortField("rsp",2)] 

    """
	def post_build(self, p, pay):
	        if self.len is None and pay:
	            l = len(pay)
	            p = p[:1] + hex(l)[2:]+ p[2:]
	        return p+pay
	"""

#bind_layers(Ether, IP)
#bind_layers(IP, UDP)
bind_layers(SPCK, UDP)

#not sure if needed
#bind_layers(IP, spellCheckPacket,  frag=0, proto=0x800)
#bind_layers(spellCheckPacket, Ether)