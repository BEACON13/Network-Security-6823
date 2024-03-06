#!/usr/bin/env python3

from scapy.all import *

ttl = 1
while True:
    a = IP(dst='8.8.8.8', ttl=ttl)
    b = ICMP()
    p = a/b
    pkt = sr1(p, verbose=0, timeout=3)
    
    if pkt is None:
        print("No reply for TTL:", ttl)
        if ttl > 15:
            break
    elif pkt.type == 0:
        print("Complete", pkt.src)
        break
    else:
        print("TTL: %d, Source:" % ttl, pkt.src)
    ttl += 1
