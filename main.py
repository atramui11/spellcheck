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
    #start net w simple switch w.o. bmv2
    print "running main..."
    topoObj = SingleSwitchTopo(2)
    net = Mininet(topo = topoObj, controller = OVSController)
    net.start()
    s1,h1,h2 = net.get('s1'), net.get('h1'),net.get('h2')

    #start server process
    server = h1.popen('./server.py', stdout=sys.stdout, stderr=sys.stdout)

    time.sleep(3) #delay server before starting client 

    #print "\n\ngot here 2 \n\n"

    #start client process    
    client = h2.cmd('sudo python client.py', stdout=sys.stdout, stderr=sys.stdout) 

    #print "\n\ngot here 3, out is: " + client + "\n\n"


    time.sleep(3) #delay before starting mininet

    # Start mininet CLI to interactively run cmds in the network:
    CLI(net)

    net.stop()

    ############P4 RUNTIME CALLS##########
   	#P4 program to forward packets to the right place
    #server 500
    #client 501
    
    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
        match_fields = {'standard_metadata.ingress_port': 500},
        action_name = 'MyIngress.set_egress_spec',
        action_params = {'port': 501})
    
    print "OK"
    
    """
	#Populating dictionary table
    #for each dictionary entry in dictionary.json:
    switch.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})
    ######################################
	"""





if __name__=="__main__":
    main()

