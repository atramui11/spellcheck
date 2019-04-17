#from p4app import P4Mininet
import sys
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from scapy import all as scapy
from mininet.topo import SingleSwitchTopo
#from spellCheckPacket import spellCheckPacket
import time


################################# MAIN ###################################

def main():
    #simple switch w.o. bmv2
    print "running main..."

    topoObj = SingleSwitchTopo(2)

    net = Mininet(topo = topoObj)

    net.start()

    s1,h1,h2 = net.get('s1'), net.get('h1'),net.get('h2')

    server = h1.popen('./server.py', stdout=sys.stdout, stderr=sys.stdout)


    time.sleep(0.4) #server delayed, listening before starting client 


    #client sends packet to server
   	#########STUCK HERE, DOES NOT GO PAST
    out = h2.cmd('python client.py') #send packet frmo h2 host node 
    
    print "out is: " + out + " this\n\n"


    """
    ############P4 RUNTIME CALLS##########
   	#P4 program to forward packets to the right place

	s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 500},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 501})

    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 501},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 500})

	#Populating dictionary table
    #for each dictionary entry in dictionary.json:
    switch.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})
    ######################################
	"""

	#time.sleep(3)
	
	# Start the mininet CLI to interactively run commands in the network:
    CLI(net) #this line only runs when xterm is called

    print "OK"



if __name__=="__main__":
    main()

