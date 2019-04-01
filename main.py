from p4app import P4Mininet
from mininet.topo import SingleSwitchTopo

topo = SingleSwitchTopo(2) #right kind of topology for spellcheck?
net = P4Mininet(program='spellcheck.p4', topo=topo)
net.start()

loss = net.pingAll()
assert loss == 0

# Start the mininet CLI to interactively run commands in the network:
from mininet.cli import CLI
CLI(net)

print "OK"
