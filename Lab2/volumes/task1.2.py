#!/usr/bin/env python3

from scapy.all import *
a = IP()
a.src = '8.8.8.8'
a.dst = '10.9.0.5'
b = ICMP()
p = a/b
send(p,iface='br-787664767f86') 
