from mininet.topo import Topo

#just one host and one switch linked together
class oneHostOneSwitchTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        
        switch1 = self.addSwitch('s1')

        host1 = self.addHost('h1', ip = "10.0.0.1", mac = '00:00:00:00:00:01')
        
        self.addLink(switch1, host1, 1, 2) #switch source port 1 to host dest. port 2