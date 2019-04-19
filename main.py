from p4app import P4Mininet
import sys
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from scapy import all as scapy
from mininet.topo import SingleSwitchTopo
import time




"""
##for adding dict entries 
def addForwardingRule(sw, host, port):
    sw.insertTableEntry(table_name='MyIngress.ipv4_lpm',
                        match_fields={'hdr.ipv4.dstAddr': ["10.0.0.%d" % host, 32]},
                        action_name='MyIngress.ipv4_forward',
                        action_params={'dstAddr': net.get('h%d' % host).intfs[0].mac,
                                          'port': port})
"""


#table entry to forward packet server-->client 
def pktFwd():
    #P4 program to forward packets to the right place
    #wire port 500 (server) to port 501 (client)
    """
    s1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
        match_fields = {'standard_metadata.ingress_port': 500},
        action_name = 'MyIngress.set_egress_spec',
        action_params = {'port': 501})
    """


################################# MAIN ###################################


def main():
    #start net w simple switch w.o. bmv2
    print "running main..."
    topoObj = SingleSwitchTopo(2)
    net = P4Mininet(program='spellcheck.p4', topo = topoObj)
    #net = Mininet(topo = topoObj)
    net.start()



    s1,h1,h2 = net.get('s1'), net.get('h1'),net.get('h2')



    """
    #Populating dictionary table
    #for each dictionary entry in dictionary.json:
    switch.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})
    """


    #start server process
    server = h1.popen('./server.py', stdout=sys.stdout, stderr=sys.stdout)

    time.sleep(3) #delay server before starting client 


    #start client process    
    client = h2.cmd('sudo python client.py', stdout=sys.stdout, stderr=sys.stdout) 

    print "\n\ngot here 3, client output is: " + client.strip() + "\n\n"


    time.sleep(3) #delay before starting mininet

    # Start mininet CLI to interactively run cmds in the network:
    CLI(net)

    net.stop()

    ############P4 RUNTIME CALLS##########
    
    print "OK"
    




if __name__=="__main__":
    main()

