#!/usr/bin/env python2

"""Client code to be run on simulation node in Mininet"""

import socket
from scapy import all as scapy
import sys

#This client operates at port 501


def main():
	print "Client running...\n"

	#creates a packet here
	pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=500)


	#This sends 1 packet
	scapy.sendp(pkt)
	print "packet sent! \n"

	#action executed when response packet has been sniffed 
	def read_packet(pkt):
		print "response has been sent back to client!\n"
		pkt.show()

	scapy.sniff(count = 1, filter = "port 501", prn=read_packet)

	sys.exit(0)

if __name__=="__main__":
    main()


