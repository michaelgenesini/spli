## IPTABLE HOW-TO

#### Virtual Machine on Mac (Virtual Box) with Ubuntu 14.04 LTS

 - set the network adapter to **BRIDGE** instead of NAT
 - run the following comand to enable forwarding of packets
```shell
$ sysctl -w net.ipv4.ip_forward=1
```
 - prepare a *sh* file with all the iptables rules like the following
```shell
#!/bin/bash
iptables -F
iptables -t nat -F
iptables -t nat -A PREROUTING -d .....
...
 ```
 - run your script `$ sudo file.sh`
 - verify your iptable configuration `$ sudo iptables -L`


#### Network configuration without Dildo

 Create an HotSpot network with manual IPv4 configuration, netmask 255.255.255.0, static IP adress (e.g. 10.10.10.10) and specify the router IP (e.g. 10.10.10.1)

### TCPDUMP
List the traffic to see all packets through your station

```shel
$ sudo tcpdump -n -i Interface host YourIP
```

Listen only icmp traffic

```shel
$ sudo tcpdump -n -i Interface icmp
```