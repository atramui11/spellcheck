#!/usr/bin/env python2

"""server code to be run on simulation node in Mininet"""


import socket
from scapy import all as scapy


#This server operates at port 500

print "Server up. Listening!...\n"

#action executed when server sniffs packet  
def read_packet(pkt):
    print "type is: " is type(pkt)
    if pkt is not None:
        print "Spellcheck packet sniffed by server!\n"
        pkt.show()

        #response back to client indicating correctness

        # 0/1
        
        print "port is: " +str(pkt[scapy.UDP].dport)

        pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=501)

        scapy.sendp(pkt)

        print "Correctness response pkt sent back to client!"


#Sniff incoming packets. this loops itself apparently 
scapy.sniff(count = 1, filter= "port 500", prn=read_packet)

