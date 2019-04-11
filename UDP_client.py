#!/usr/bin/env python2

import socket
from scapy import all as scapy
import sys
from uuid import getnode

print "client running...\n"

"""
if len(sys.argv) is not 3:
	print "numArgsin is: " + str(len(sys.argv)) + "\n"
	print "Not enough args. usage is ./prog.py dstAddr wordToCheck \n"
	sys.exit(1)
"""


wordToCheck="dogf" #str(sys.argv[1]) #mac for source node h1

print "hi1 \n"

pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=500)


print "hi2 \n"

#This sends 1 packet Scapy sendp itself creates socket
scapy.sendp(pkt)


def read_packet(pkt):
	"response has been sent back to client"
	pkt.show()

scapy.sniff(filter = "port 501", prn=read_packet)

print "packet sent! \n"

