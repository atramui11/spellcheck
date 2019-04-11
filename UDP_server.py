#!/usr/bin/env python2

import socket
from scapy import all as scapy

localIP     = "127.0.0.1"
localPort   = 500
bufferSize  = 1024


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))


print "UDP server up. Listening...\n"

def read_packet(pkt):
    print "type is: " is type(pkt)
    if pkt is not None:
        print "server received packet!\n"
        pkt.show()

        #response back to client indicating correctness
        print "port is: " +str(pkt[scapy.UDP].dport)
        scapy.sendp(pkt)

#Sniff incoming packets
while True:
    p = scapy.sniff(filter= "port 500", prn=read_packet)

