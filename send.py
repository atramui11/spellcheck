#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
import argparse

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, hexdump
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP
from myTunnel_header import SPCHK


######### CLIENT SENDS TO SERVER CODE

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        print "ifs are: " + str(i)
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_addr', type=str, help="The destination IP address to use")
    parser.add_argument('message', type=str, help="The message to include in packet")
    parser.add_argument('word', type=str, help="word to check")
    parser.add_argument('--dst_id', type=int, default=None, help='port to go to')
    args = parser.parse_args()

    addr = socket.gethostbyname(args.ip_addr)
    dst_id = args.dst_id
    word = args.word
    iface = get_if()

    """
    if (dst_id is not None):
        print "sending on interface {} to dst_id {}".format(iface, str(dst_id))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
        pkt = pkt / SPCHK(dst_id=dst_id,wordp1=0x646,wordp2=0xf67) / IP(dst=addr) / args.message
    else:
        print "sending on interface {} to IP addr {}".format(iface, str(addr))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
        pkt = pkt / IP(dst=addr) / TCP(dport=1, sport=random.randint(49152,65535)) / args.message
    """

    print "sending on interface {} to IP addr {}".format(iface, str(addr))
    pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
    #rsp=2 means iniitially incorrect
    pkt = pkt / IP(dst=addr) / TCP(dport=dst_id, sport=2) / SPCHK(rsp=2,word=word) / args.message
    
    pkt.show2()
#    hexdump(pkt)
#    print "len(pkt) = ", len(pkt)

    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
