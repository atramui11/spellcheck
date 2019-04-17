#!/usr/bin/env python

"""Server code to be run on simulation node in Mininet"""
from scapy import all as scapy
import sys

#This server operates at port 500

print "Server up. Listening!...\n"

#action executed when server sniffs packet  
def read_packet(pkt):
    if pkt is not None:
        portno = pkt[scapy.UDP].dport #int

        #server port
        if portno==500:
            print "Server has received spellcheck pkt from client: \n\n"
            pkt.show()
            print "\n\n"

            #send 0/1 rsp back to client indicating correctness via pkt fwding using P4
            pkt = scapy.Ether()/scapy.IP(dst="10.0.0.2",ttl=5)/scapy.UDP(dport=501)
            scapy.sendp(pkt)

        #client port
        if portno==501:
            print "Client receieved correctness response pkt: \n\n"
            pkt.show()
            print "\n\n"
        

#Sniff incoming packets. this loops itself apparently 
scapy.sniff(count = 2, filter= "portrange 500-501", prn=read_packet)

