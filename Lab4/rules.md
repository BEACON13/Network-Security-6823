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

# 6
``` shell
sudo iptables -A OUTPUT -p icmp -d 8.8.8.8 -j LOG --log-prefix "ICMP to Google! "
```

# 7
Above all, set the default policy to DROP for the INPUT, OUTPUT, and FORWARD chains.

Step 1: Allow any outgoing traffic from the 192.168.60.0/24 network to the 10.9.0.0/24 network
This rule allows outgoing connections initiated from the 192.168.60.0/24 network to the 10.9.0.0/24 network, ensuring that the connections are stateful (tracking both new and established connections).
``` shell
iptables -A FORWARD -s 192.168.60.0/24 -d 10.9.0.0/24 -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -s 10.9.0.0/24 -d 192.168.60.0/24 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

Step 2: Allow any host to ping the router (10.9.0.11 or 192.168.60.11)
To allow ICMP echo requests (pings) to both interfaces of the router and ensure replies are sent back, we'll set rules in both the INPUT and OUTPUT chains, also using connection tracking for stateful management.
``` shell
# Allow pinging the router's external IP
iptables -A INPUT -d 10.9.0.11 -p icmp --icmp-type echo-request -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -s 10.9.0.11 -p icmp --icmp-type echo-reply -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow pinging the router's internal IP
iptables -A INPUT -d 192.168.60.11 -p icmp --icmp-type echo-request -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -s 192.168.60.11 -p icmp --icmp-type echo-reply -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

Step 3: Allow host 10.9.0.5 to telnet to 192.168.60.5
This rule specifically allows telnet traffic (TCP on port 23) from 10.9.0.5 to 192.168.60.5, employing connection tracking to manage the state of the connection.
``` shell
iptables -A FORWARD -s 10.9.0.5 -d 192.168.60.5 -p tcp --dport 23 -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -s 192.168.60.5 -d 10.9.0.5 -p tcp --sport 23 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```