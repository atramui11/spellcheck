from p4app import P4Mininet
import sys
from mininet.net import Mininet
from mininet.cli import CLI
from scapy import all as scapy
from mininet.topo import SingleSwitchTopo
import time



##for adding dict entries 
def addForwardingRule(sw, host, port, addr):
    sw.insertTableEntry(table_name='MyIngress.ipv4_lpm',
                        match_fields={'hdr.ipv4.dstAddr': ["10.0.0.%d" % host, 32]},
                        action_name='MyIngress.ipv4_forward',
                        action_params={'dstAddr': addr, 'port': port})


def addTunnelFwd(sw, d_id, port2):
    sw.insertTableEntry(table_name='MyIngress.myTunnel_exact',
                        match_fields={'hdr.myTunnel.dst_id': [d_id]},
                        action_name='MyIngress.myTunnel_forward',
                        action_params={'port': port2})


"""
def populateDictTable(sw)
    #for each dictionary entry in dictionary.json:
        sw.insertTableEntry(table_name = 'MyIngress.word_dictionary',
                        match_fields = {'hdr.word_to_check.spellcheck_word': ???},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})
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
    
    addr1 = h1.intfs[0].mac #h1 server mac addr
    addr2 = h2.intfs[0].mac #h2 client mac addr

    #Do I need to set default action to drop? think its done already. 
    addForwardingRule(s1,1,1,addr1) #server (1) receives packet. want to bounce it back to client (2)
    addForwardingRule(s1,2,2,addr2) #packet headed to client routed back to client and gets port 2

    addTunnelFwd(s1,1,1) #dst id 1 gets egressSpec 'port' of 1
    addTunnelFwd(s1,2,2) #dst id 2 gets egressSpec 'port' of 2

    #P4 program to forward packets to the right place
    #need to fwd pkt from port 1 (server) to port 2 (client)
    #dstAddr = h1.intfs[0].mac
    #print "dstAddr: " + str(h1.intfs[0])
    
    # table that will match on the input port and set the output egress_spec
    """
    s1.insertTableEntry(table_name='MyIngress.portFwd',
                        match_fields={'standard_metadata.ingress_port': 1},
                        action_name='MyIngress.set_egress_spec',
                        action_params={'port':2})
    """


    #server 10.0.0.1 client 10.0.0.2
    #############  SERVER
    server = h1.popen('./receive.py', stdout=sys.stdout, stderr=sys.stdout)
    time.sleep(0.4) #delay server before starting client 
    

    #############  CLIENT sends word to server w tunneled header
    client = h2.cmd('./send.py --dst_id 1 10.0.0.1 "AA" ', stdout=sys.stdout, stderr=sys.stdout) 
    #client = h2.cmd('./send.py 10.0.0.1 "AA"', stdout=sys.stdout, stderr=sys.stdout)     
    print "\n\n client send says: \n\n" + client.strip() + "\n\n"

    time.sleep(8) #delay for server to receive and forward packet via P4

    #############  MININET
    CLI(net) 
    

    #############  END
    net.stop()
    print "OK"



if __name__=="__main__":
    main()

