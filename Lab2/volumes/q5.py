#!/usr/bin/env python3
from scapy.all import *

def sniff_and_spoof(packet):
    if ICMP in packet and packet[IP].dst == "10.9.0.99":
        ip = IP(src = packet[IP].dst, dst = packet[IP].src)
        icmp = ICMP(type = 0, id = packet[ICMP].id, seq = packet[ICMP].seq)
        
        raw_data = packet[Raw].load
        newpacket= ip/icmp/raw_data
        
        send(newpacket,verbose=0)
        
pkt = sniff(iface='br-01581d39dca4',filter="icmp and dst host 10.9.0.99", prn=sniff_and_spoof)

