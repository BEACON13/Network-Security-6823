# Default rules
Drop everything
```shell
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
```

# 2B
``` shell
# Block ICMP echo requests coming from the external network to the internal network
iptables -A FORWARD -p icmp --icmp-type echo-request -i eth0 -o eth1 -j DROP

# Allow ICMP echo requests from internal network to external network
iptables -A FORWARD -p icmp --icmp-type echo-request -i eth1 -o eth0 -j ACCEPT

# Allow ICMP echo replies from external network to internal network
iptables -A FORWARD -p icmp --icmp-type echo-reply -i eth0 -o eth1 -j ACCEPT

iptables -A INPUT -p icmp --icmp-type echo-request -i eth0 -j ACCEPT

iptables -A OUTPUT -p icmp --icmp-type echo-reply -o eth0 -j ACCEPT
```

# 2C
``` shell
# 外部可以访问192.168.60.5的23端口 telnet
iptables -A FORWARD -p tcp -d 192.168.60.5 --dport 23 -i eth0 -o eth1 -j ACCEPT

# 192.168.60.5可以通过23端口访问外部 telnet
iptables -A FORWARD -p tcp -s 192.168.60.5 --sport 23 -i eth1 -o eth0 -j ACCEPT

# 允许内部访问内部
iptables -A FORWARD -p tcp -s 192.168.60.0/24 -d 192.168.60.0/24 -i eth1 -o eth1 -j ACCEPT
```

# 3B
``` shell
# Add these 2 new rules to 2C
iptables -A FORWARD -m conntrack --ctstate NEW,ESTABLISHED -s 192.168.60.0/24 -o eth0 -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED -i eth0 -d 192.168.60.0/24 -j ACCEPT
```