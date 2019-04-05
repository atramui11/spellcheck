from mininet.topo import Topo

#just one host and one switch linked together
class oneHostOneSwitchTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        
        host1 = self.addHost('h1', ip = "10.0.0.1", mac = '00:00:00:00:00:01')
        switch1 = self.addSwitch('s1')
        self.addLink(host1, switch1, port2=1)