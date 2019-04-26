from p4app import P4Mininet
import sys
from mininet.net import Mininet
from mininet.cli import CLI
from scapy import all as scapy
from mininet.topo import SingleSwitchTopo
import time
import json


"""
##for adding dict entries 
def addForwardingRule(sw, host, port, addr):
    sw.insertTableEntry(table_name='MyIngress.packetForward',
                        match_fields={'hdr.ipv4.dstAddr': ["10.0.0.%d" % host, 32]},
                        action_name='MyIngress.packetForward',
                        action_params={'dstAddr': addr, 'port': port})
"""

"""
s1.insertTableEntry(table_name='MyIngress.portFwd',
                    match_fields={'standard_metadata.ingress_port': 1},
                    action_name='MyIngress.set_egress_spec',
                    action_params={'port':2})
"""




##############WORD TO SPELLCHECK

#
#inputWord = "yog"
matchSize = 4 #how many bytes P4 compiler puts in each table entry 
#

########################

#P4 Program to forward packets to the right place
def addForwardingRule(sw, sport, dport):
    sw.insertTableEntry(table_name='MyIngress.packetForward',
                        match_fields={'hdr.tcp.srcPort': [sport]},
                        action_name='MyIngress.pkt_fwd',
                        action_params={'dport': dport})


#P4 Table Entries for matching SPCHK.word header for spellcheck
def populateDictTable(sw):
    #load dictionary.json into a list

    data = None
    with open('dictionary.json') as json_file:  
        data = json.load(json_file)

    #each p is a word to install in the table
    for p in data:
               
        if len(str(p)) is matchSize:
            print "installing entry: " + str(p)
            word1 = str(p)
            sw.insertTableEntry(table_name = 'MyIngress.wordDict%d'%matchSize,
                    match_fields = {'hdr.spchk.spchk%d.word'%matchSize :word1},
                    action_name = 'MyIngress.installWordEntry%d'%matchSize,
                    action_params = {'resp' : 1})
    

    

    #single test words
    """
    word1 = "glut" 
    sw.insertTableEntry(table_name = 'MyIngress.wordDict4',
                    match_fields = {'hdr.spchk.spchk4.word':word1},
                    action_name = 'MyIngress.installWordEntry4',
                    action_params = {'resp' : 1})
    

    word2 = "dog" 
    sw.insertTableEntry(table_name = 'MyIngress.wordDict3',
                    match_fields = {'hdr.spchk.spchk3.word':word2},
                    action_name = 'MyIngress.installWordEntry3',
                    action_params = {'resp' : 1})

    word3 = "to" 
    sw.insertTableEntry(table_name = 'MyIngress.wordDict2',
                    match_fields = {'hdr.spchk.spchk2.word':word3},
                    action_name = 'MyIngress.installWordEntry2',
                    action_params = {'resp' : 1})
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

    #this line specifically causes server to receive packet. tcp sport 2-->tcp dport 1 
    addForwardingRule(s1,2,1) #client to server forwarding
    #addForwardingRule(s1,1,2)

    #fill dictionary table here
    populateDictTable(s1)


    #dstAddr = h1.intfs[0].mac
    

    #server 10.0.0.1 client 10.0.0.2
    #############  SERVER
    server = h1.popen('./receive.py', stdout=sys.stdout, stderr=sys.stdout)
    time.sleep(0.4) #delay server before starting client 
    

    #############  CLIENT sends words to server (1)
    inputWord = "glut"
    client = h2.cmd('./send.py 10.0.0.1 "PAYLOAD" %s --dst_id 1' % inputWord, stdout=sys.stdout, stderr=sys.stdout)     
    print "\n\n client send says: \n\n" + client.strip() + "\n\n"


    inputWord = "card"
    client = h2.cmd('./send.py 10.0.0.1 "PAYLOAD" %s --dst_id 1' % inputWord, stdout=sys.stdout, stderr=sys.stdout) 
    print "\n\n client send says: \n\n" + client.strip() + "\n\n"

    inputWord = "yope"
    client = h2.cmd('./send.py 10.0.0.1 "PAYLOAD" %s --dst_id 1' % inputWord, stdout=sys.stdout, stderr=sys.stdout) 
    print "\n\n client send says: \n\n" + client.strip() + "\n\n"

    inputWord = "yolk"
    client = h2.cmd('./send.py 10.0.0.1 "PAYLOAD" %s --dst_id 1' % inputWord, stdout=sys.stdout, stderr=sys.stdout) 
    print "\n\n client send says: \n\n" + client.strip() + "\n\n"



    time.sleep(4) #delay for server to receive and forward packet via P4

    #############  MININET
    #CLI(net) 
    

    #############  END
    net.stop()
    print "OK"



if __name__=="__main__":
    main()

