import struct
UDP_PORT = 12

#spellCheckHeader 
spChkReqHdr = struct.Struct('!B') # key 

#responseHeader
spChkResHdr = struct.Struct('!I') #value (0/1)
