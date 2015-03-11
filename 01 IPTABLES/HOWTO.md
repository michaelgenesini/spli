## IPTABLE HOW-TO

#### Virtual Machine on Mac (Virtual Box) with Ubuntu 14.04 LTS

 - set the network adapter to **BRIDGE** instead of NAT
 - run the following comand to enable forwarding of packets
 ```
 	$ sysctl -w net.ipv4.ip_forward=1
 ```
 - prepare a *sh* file with all the iptables rules like the following
```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```
```shell
#!/bin/bash
iptables -F
iptables -t nat -F
iptables -t nat -A PREROUTING -d .....
...
 ```
 - launch your script `$ sudo file.sh`
 - verify your iptable configuration `$ sudo iptables -L`


### TCPDUMP
List the traffic to see all packets through your station

```
$ sudo tcpdump -n -i eth0 host YourIP
```
