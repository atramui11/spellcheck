#!/usr/bin/env python

import sys
import socket
from spellcheck_protocol import *

print "running server (node h1)..."

#server binds to socket at UDP_PORT
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', UDP_PORT))


#this will hold all the dictionary entries
store = {1: 1001, 2: 2002, 3:3003}


#server loop run
while True:
	#keep on receive data from the socket. 1024 is just buffer size not addr
    request, addr = s.recvfrom(1024)
    wordToSpellcheck, = spChkReq.unpack(req)

    print addr, "Request (word): (%d),"% wordToSpellcheck,

    #YES response 
    if  wordToSpellcheck in store:
        value = 1
        print "Response (correctness): (%d)" % value
    else:
    #NO response
        value = 0
        print "word spellcheck negative"

    #send response back to socket addr, back to client
    response = spChkResHdr.pack(value)
    s.sendto(response, addr)

