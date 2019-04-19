#!/usr/bin/env python

"""Client code to be run on simulation node in Mininet"""
from scapy import all as scapy
import sys
from spellCheckPacket import spellCheckPacket

#This client operates at port 501

def clientProcess():
	#create special spellcheck packet here
	pkt = scapy.Ether()/scapy.IP(dst="10.0.0.1",ttl=5)/scapy.UDP(dport=500)

	#Send spellcheck pkt
	scapy.sendp(pkt)
	print "packet sent in client.py! \n"
	return 0

def main():
	return clientProcess()
	

if __name__=="__main__":
    main()


