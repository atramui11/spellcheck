#!/usr/bin/env python

"""Client code to be run on simulation node in Mininet"""
from scapy import all as scapy
from spellCheckPacket import SPCK

#This client operates at port 501

def clientProcess():
	#create special spellcheck packet here
	#server needs to change rsp field to 1 if found in dict table

	spckpkt=SPCK() #spw='dog', rsp=2


	eth = scapy.Ether()
	ip = scapy.IP(dst="10.0.0.1",ttl=5)
	udp = scapy.UDP(sport=501,dport=500)
	#spck = SPCK(word='water',rsp=1)
	
	pkt = eth/ip#/udp#/spck

	pkt.show()

	#portno = pkt[scapy.UDP].dport
	#print "dst portno before send is: " + str(portno)

	print "above is custom packet before being sent. \n\n\n"
	
	#Send spellcheck pkt
	scapy.sendp(pkt)
	print "packet sent in client.py! \n"
	return 0

def main():
	return clientProcess()
	

if __name__=="__main__":
    main()


