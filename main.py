#FLOW OF CONTROL: p4app run triggers ONLY this file, main.py


##########NOTES#############

"""
client needs to send packets to topo object, which is the switch itself

Mininet object is 'net' made from 'topo', so could I tie a Client class to 'net'?

Client class would need to send a word packet to 'topo' using word_to_check header I defined in spellcheck.p4, so Client class would need to know about spellcheck.p4 too. would this be through 'topo'?
"""


"""
'net' is the Mininet network simulation CONTAINING p4 specs of spellcheck.p4
i.e. spellcheck.p4 is the contract b/w control plane and data plane(s) in this given network simulation 'net'
"""


from p4app import P4Mininet
from mininet.topo import SingleSwitchTopo
import sys


#doesnt get anything IN from p4 file....
#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)


topo = SingleSwitchTopo(2) #arg is num of hosts for this single switch
net = P4Mininet(program='spellcheck.p4', topo=topo)

net.start()


loss = net.pingAll()
assert loss == 0

# Start the mininet CLI to interactively run commands in the network:
from mininet.cli import CLI #mininet terminal gets up to here until calling xterm

CLI(net) #this line only runs when xterm is called

print "OK"
