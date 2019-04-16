#!/usr/bin/env python2

"""server code to be run on simulation node in Mininet"""


import socket
from scapy import all as scapy


#This server operates at port 500

print "Server up. Listening...\n"

#action executed when packet is sniffed 
def read_packet(pkt):
    print "type is: " is type(pkt)
    if pkt is not None:
        print "Packet received by server!\n"
        pkt.show()

        #response back to client indicating correctness
        print "port is: " +str(pkt[scapy.UDP].dport)

        pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=501)

        scapy.sendp(pkt)

#Sniff incoming packets. this loops itself apparently 
scapy.sniff(count = 1, filter= "port 500", prn=read_packet)

