#!/usr/bin/env python3
from scapy.all import *
def print_pkt(pkt):
    pkt.show()

# Capture only ICMP packet
# pkt = sniff(iface='br-787664767f86', filter='icmp', prn=print_pkt)

# Capture any TCP packet that comes from a specific IP and with a destination port number 23
# pkt = sniff(iface='br-787664767f86', filter='tcp && src host 10.9.0.5 &&  dst port 23',  prn=print_pkt)

# Capture packets coming from or going to a subnet 10.9.0.0/24.
pkt = sniff(iface='br-787664767f86', filter='net 10.9.0.0/24',  prn=print_pkt)
