import socket
from scapy import all as scapy

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

#msgFromServer = "dogf"
#bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
 

print("UDP server up. Listening...")

# Listen for incoming packets
while(True):

    #use Scapy to sniff single incoming packet
    p = scapy.sniff(filter = 'dst port 20001')

    print(p)
    if p is not None:
        print("server received packet, it is : ", p)

        #response back to client indicating correctness
        #scapy.send(scapy.IP(dst="127.0.0.1")/scapy.UDP(dport=20001))

