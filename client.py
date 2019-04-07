#!/usr/bin/env python

import sys
import socket
from spellcheck_protocol import *

#example use: ./client.py host wordToSpellcheck

host = sys.argv[1]
wordToSpellcheck = int(sys.argv[2]) #word for spellcheck

addr = (host, UDP_PORT)

#have to open socket to server on client side
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

#send word to host as a request
request = spChkReqHdr.pack(wordToSpellcheck)
s.sendto(request, addr)

#problem here, no response, times out
response, addr2 = s.recvfrom(1024)

value = spChkResHdr.unpack(response)

print "client response is: " + value