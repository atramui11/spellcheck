#!/usr/bin/env python2

"""Client code to be run on simulation node in Mininet"""


import socket
from scapy import all as scapy
import sys

#This client operates at port 501

print "Client running...\n"


#if len(sys.argv) is not 3:
	#print "numArgsin is: " + str(len(sys.argv)) + "\n"
	#print "Not enough args. usage is ./prog.py dstAddr wordToCheck \n"
	#sys.exit(1)


wordToCheck="dogf"


#creates a packet here
pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=500)


#This sends 1 packet
#Sendp itself creates a socket 
scapy.sendp(pkt)
print "packet sent! \n"


#action executed when response packet has been sniffed 
def read_packet(pkt):
	print "response has been sent back to client!\n"
	pkt.show()

scapy.sniff(count = 1, filter = "port 501", prn=read_packet)

#ends 
