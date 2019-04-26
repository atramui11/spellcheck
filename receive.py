#!/usr/bin/env python
import sys
import struct
import os

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption, Ether
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, TCP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR
from myTunnel_header import SPCHK


#SERVER RECEIVING CODE 


def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find h1-eth0 interface"
        exit(1)
    return iface

#client 2 and server 1 packet handling code
def handle_pkt(pkt):
    if SPCHK in pkt and (TCP in pkt and pkt[TCP].dport == 1):
        print "\n\n\nSERVER RECEIVED PACKET. WORD LENGTH IS: \n\n" + str(len(pkt[SPCHK].word))
        print "word is: \n"
        for elem in pkt[SPCHK].word:
            print elem
        pkt.show2()

        #if there is a match in P4 table wordDict P4 code should send back pkt to client rsp=1
        if pkt[SPCHK].rsp is 1:
            print "\n\n\nSPELLCHECKED, WORD IS CORRECT\n\n\n"
            iface = get_if()
            pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
            pkt = pkt / IP(dst="10.0.0.2") / TCP(dport=2) / SPCHK(length=1, word="Y", rsp=1) / "PAYLOAD"
            #pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
        else:
            #no match, send back pkt with rsp = 0
            print "\n\n\nWORD FAILED SPELLCHECK\n\n\n"
            iface = get_if()
            pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
            pkt = pkt / IP(dst="10.0.0.2") / TCP(dport=2) / SPCHK(length=1,word="N",rsp=0) / "PAYLOAD"
            #pkt.show2()
            sendp(pkt, iface=iface, verbose=False)

#        hexdump(pkt)
#        print "len(pkt) = ", len(pkt)
        sys.stdout.flush()
    elif SPCHK in pkt and (TCP in pkt and pkt[TCP].dport == 2):
        print "\n\n\nCLIENT RECEIVED PACKET THAT SAYS:\n"
        pkt.show2()

            

def main():
    print "\n\nServer Running..." + str(os.listdir('/sys/class/net/'))
    ifaces = filter(lambda i: 'eth0' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print "\n\nsniffing on %s" % iface
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
