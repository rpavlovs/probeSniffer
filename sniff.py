#!/usr/bin/env python
from scapy.all import *
import sys

interface = str(sys.argv[1])
target_addr = '78:31:c1:30:a1:e6'

# Add some colouring for printing packets later
GREEN = '\033[92m'
END = '\033[0m'

def sniffProbes(p):
	src = p[Dot11].addr2
	subtype = p[Dot11].subtype
	seq = p[Dot11].SC

	if (src == target_addr and (subtype == 4 or subtype == 5)) :
		channel = int(ord(p[Dot11Elt:4].info))
        	rssi = (ord(p.notdecoded[-4:-3])-256)
		
		if (channel == 1) :
			print( GREEN
				+ 'SRC: ' 				+ str(src)		+ '\t'
				+ 'Channel: ' 			+ str(channel)	+ '\t'
				+ 'RSSI: ' 				+ str(rssi)		+ '\t'
				+ 'Seqence number: '	+ str(seq)		+ '\t'
				+ END )

sniff(iface=interface, prn=sniffProbes)
