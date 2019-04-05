from p4app import P4Mininet
import sys
from mininet.cli import CLI
from topology import oneHostOneSwitchTopo
from scapy.all import sendp
#from scapy.all import Packet, Ether, IP, ARP

from spellCheckWord import spellCheckPacket



#global temporarily
host1 = None 
switch1= None

def receivePacket():
    print "receiving packet" 


def setUpTables(switch):
    #need to make sure ports are correct 
    switch.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 1},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 2})

    switch.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 2},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})


    #can do this later once packet send is working
    #necessary to populate switch w/ ALL dict entries from .json ? then:
    #for each dictionary entry in dictionary.json:
    """switch.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})"""


def main():
    #instantiate the (s1,h1) topology
    topoObject = oneHostOneSwitchTopo()

    #start net object with (s1,h1) topology and P4 specifications
    net = P4Mininet(program='spellcheck.p4', topo=topoObject)
    net.start()


    #host node just in case
    host1 = net.get('h1')

    #set up switch match action table to send and receive at port 1
    switch1 = net.get('s1') #switch node object
    
    setUpTables(sw1) #make sure this topo is set b4 sending packet
    
    #send packet using Scapy
    #spkt = spellCheckPacket() 
    #sendp(spkt) #sendp fx works at layer 2 


    #first just gen packet and send to test code

    #generate(custom_packet)

    #send custom_packet(host1, switch1)
        """
        based on the .p4 file, after receiving the packet
        switch should match on the 'special' (here, spellcheck) header 
        to search into the dict table (for which eventually will add entries) 
        """

    #simple 0/1 response back indicating correctness
        #could probably use spellCheckPacket() again
        #temp = generatepacket(based on previous search result)

    #send temp(switch1, host1)


    # Start the mininet CLI to interactively run commands in the network:
    CLI(net) #this line only runs when xterm is called

    print "OK"



if __name__=="__main__":
    main()

