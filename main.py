from p4app import P4Mininet
from mininet.topo import Topo
import sys


class oneHostOneSwitchTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        
        #add one host, one switch, and link them
        host1 = self.addHost('h1', ip = "10.0.0.1", mac = '00:00:00:00:00:01')
        switch1 = self.addSwitch('s1')
        self.addLink(host1, switch1, port2=1)

def main():
    #instantiate the (s1,h1) topology
    topoObject = oneHostOneSwitchTopo()

    #start net object with (s1,h1) topology and P4 specifications
    net = P4Mininet(program='spellcheck.p4', topo=topoObject)
    net.start()


    # Start the mininet CLI to interactively run commands in the network:
    from mininet.cli import CLI #mininet term gets up to here until calling xterm


    #host node just in case
    h1 = net.get('h1')

    #set up switch match action table
    sw1 = net.get('s1') #switch node
    sw1.insertTableEntry(table_name = 'MyIngress.oneHostoneSwitch',
                        match_fields = {'standard_metadata.ingress_port': 1},
                        action_name = 'MyIngress.set_egress_spec',
                        action_params = {'port': 1})


    CLI(net) #this line only runs when xterm is called

    print "OK"

if __name__=="__main__":
    main()






##########NOTES#############

"""
    client needs to send packets to topo object, which is the switch itself
    
    Mininet object is 'net' made from 'topo', so could I tie a Client class to 'net'?
    
    Client class would need to send a word packet to 'topo' using word_to_check header I defined in spellcheck.p4, so Client class would need to know about spellcheck.p4 too. would this be through 'topo'?
    
    'net' is the Mininet network simulation CONTAINING p4 specs of spellcheck.p4
    i.e. spellcheck.p4 is the contract b/w control plane and data plane(s) in this given network simulation 'net'
    """


#COMPILE ONLY (P4_16)
"""
    import sys
    from p4app import P4Program
    import json
    
    prog16 = P4Program('spellcheck.p4')
    prog16.compile()
    
    # Inspect the compiled JSON file
    with open(prog16.json(), 'r') as f:
    bmv2_json = json.load(f)
    print bmv2_json['actions']
    """
