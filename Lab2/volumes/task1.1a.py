#!/usr/bin/env python3
from scapy.all import *
def print_pkt(pkt):
    pkt.show()

# Capture only ICMP packet
pkt = sniff(iface='br-787664767f86', filter='icmp', prn=print_pkt)
