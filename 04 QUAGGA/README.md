# 4: QUAGGA

All users have to enable the ip forwarding

```shell
$ sysctl -w net.ipv4.conf.all.forwarding=1
```

![network](https://copy.com/ekx7O7YPnnY47mpf)

### IPs - (manual settings)

Mike Router
	wifi 	192.168.13.3/24

Marci
	wifi 		192.168.13.2
	eth			192.168.12.2

Pedro
	wifi		192.168.13.1
	eth			192.168.12.1

-----

### Zebra - interface declaration and static routing

#### Mike:

```shell
interface wlan0
 ip address 192.168.13.3/24
```

#### Pedro:
```shell
interface eth0
 ip address 192.168.12.1/24
 ipv6 nd suppress-ra
!
interface lo
 ip address 192.168.30.1/24
!
interface wlan0
 ip address 192.168.13.1/24
 multicast
 ipv6 nd suppress-ra
```

#### Marci:
```shell
interface eth0
 ip address 192.168.12.2/24
 ipv6 nd suppress-ra
!
interface lo
 ip address 192.168.20.2/24
!
interface wlan0
 ip address 192.168.13.2/24
 multicast
 ipv6 nd suppress-ra
```

### BGP - **Border Gateway Protocol** routing protocol (between autonomous system)

#### Mike:
```shell
router bgp 34
 bgp router-id 3.3.3.3
 neighbor 192.168.13.2 remote-as 50
 neighbor 192.168.13.1 remote-as 7675
```

#### Pedro:

```shell
router bgp 7675
 bgp router-id 1.1.1.1
 network 192.168.30.0/24
 neighbor 192.168.12.2 remote-as 50
 neighbor 192.168.12.2 next-hop-self
 neighbor 192.168.13.3 remote-as 34
 neighbor 192.168.13.3 next-hop-self
```

#### Marci:

```shell
router bgp 50
 bgp router-id 192.168.20.2
 network 192.168.20.0/24
 neighbor 192.168.12.1 remote-as 7675
 neighbor 192.168.12.1 next-hop-self
 neighbor 192.168.13.3 remote-as 34
 neighbor 192.168.13.3 next-hop-self
```

### OSPF - **Open Shortest Path First** routing protocol (within a single autonomous system)

#### Pedro:

 ```shell
interface eth0
!
interface lo
!
interface wlan0
! ip ospf message-digest-key 1 md5 hallo123
!
router ospf
 ospf router-id 1.1.1.1
 network 192.168.12.0/24 area 0.0.0.0
 network 192.168.30.0/24 area 0.0.0.0
 ```

#### Marci:

```shell
interface eth0
!
interface lo
!
interface wlan0
!
router ospf
 ospf router-id 2.2.2.2
 network 192.168.12.0/24 area 0.0.0.0
 network 192.168.20.0/24 area 0.0.0.0
 ```
 ----

### TEST
pedro ping -S 192.168.30.1 192.168.20.2

mike tcpdump vede il redirect solo se staccano ethernet tra loro
