import socket
from scapy import all as scapy


UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 20001
bufferSize = 1024
msg = "dogf"


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
#UDPClientSocket.sendto(bytesToSend, serverAddressPort)

#here send to server using scapy and UDP socket
#sends 1 packet and receive response

pkt = scapy.IP(dst="127.0.0.1")/scapy.UDP(dport=20001)

#connect to addressport and send packet
UDPClientSocket.connect(("127.0.0.1",20001))
UDPClientSocket.send(bytes(pkt))

