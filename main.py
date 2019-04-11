from p4app import P4Mininet
import sys
from mininet.cli import CLI
from scapy import all as scapy
from mininet.topo import SingleSwitchTopo
#from spellCheckPacket import spellCheckPacket
import time


################################# MAIN ###################################

def main():
    #one switch, two hosts
    #instantiate the (s1 (switch), h1 (server), h2 (client)) topology
    topoObject = SingleSwitchTopo(2)

    #start net object with (s1,h1) topology and P4 specifications
    net = P4Mininet(program='spellcheck.p4', topo=topoObject)
    net.start()

    #switch, server, client
    s1,h1,h2 = net.get('s1'), net.get('h1'),net.get('h2')



    ###########SET UP TOPOLOGY USING P4 MATCH ACTION TABLES###########
    #this should make the following connections: 1-->2 and 2-->1 
    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 500},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 501})

    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 501},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 500})


    """
    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 2},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})
    """

    #LATER: POPULATE DICTIONARY TABLE 
    #for each dictionary entry in dictionary.json:
    """switch.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})"""
    ###########################################################


    #run UDP server on h1
    UDPserver = h1.popen('./UDP_server.py', stdout=sys.stdout, stderr=sys.stdout)

    #serverMAC = str(h1.cmd('python getMAC.py'))

    time.sleep(0.4) #server delayed, listening before starting client 





    #SEND CLIENT REQUEST ON CLIENT NODE H2 to send packet
    out = h2.cmd('python UDP_client.py') #send packet frmo h2 host node 
    
    print "out is: " + out.strip() + "\n\n"
    #assert out.strip() == "1001"


    time.sleep(10)

    # Start the mininet CLI to interactively run commands in the network:
    #CLI(net) #this line only runs when xterm is called



    UDPserver.terminate()

    print "OK"



if __name__=="__main__":
    main()

