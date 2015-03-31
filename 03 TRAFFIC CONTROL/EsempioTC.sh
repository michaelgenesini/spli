# config
device="br0"
lan_ip="192.168.2.131"

inet_burst="6k"

inet_up="100000bit"
inet_down="100000bit"


# reset everything
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables -t nat -F
iptables -t mangle -F
tc qdisc del dev $device root 2> /dev/null
iptables -F POSTROUTING -t mangle



# Classes:
#
#      1:  (qdisc)
#      |
#      |----|----|
#      |    |    | (inet down, inet up)
#      |    |    |
#      |    |    |
#      |    |    1:13  inet_down(13) (Webinterfaces, SSH, WLAN, all other traffic)
#      |    |
#      |    |
#      |    1:12 inet_up(12)  (Webinterfaces, SSH, WLAN, all other traffic)
#      |
#      |
#      1:11 lan_traffic (11)

echo "setting up tc qdisc and classes..."


#Tutto il traffico non classificato in altro modo è assegnato alla classe 1:13
tc qdisc add dev ${device} root handle 1: htb default 13

#Associa ad ogni classe (11, 12, 13) una certa banda
echo "1:11..." && tc class add dev ${device} parent 1:  classid 11 htb rate 1tbps burst 12k
echo "1:12..." && tc class add dev ${device} parent 1:  classid 12 htb rate ${inet_up} burst ${inet_burst}
echo "1:13..." && tc class add dev ${device} parent 1:  classid 13 htb rate ${inet_down}   burst ${inet_burst}


#Gestisce ogni mangle con priorità e basta non fa niente con netem o ftb 
# put marks from IPTABLES to the right classes
echo "adding tc filters to map iptables to classes..."
tc filter add dev ${device} parent 1:0 prio 3 protocol ip handle 11 fw flowid 1:11
tc filter add dev ${device} parent 1:0 prio 2 protocol ip handle 12 fw flowid 1:12
tc filter add dev ${device} parent 1:0 prio 2 protocol ip handle 13 fw flowid 1:13

# high priorty inet mark
#tc filter add dev ${device} protocol ip prio 1 handle 22 fw classid 12
#tc filter add dev ${device} protocol ip prio 1 handle 23 fw classid 13



echo "adding iptables rules..."

# POSTROUTING for upload traffic


echo "lan and vpn..." # needs to be the last rule, so put it on top here
iptables -I POSTROUTING -s "192.168.2.0/24" -d "192.168.2.0/24" -t mangle -j MARK --set-mark 11 # 0xb

echo "wlan, downloads, everything else..."
iptables -I POSTROUTING -s ${lan_ip} -t mangle -j MARK --set-mark 12 # 0xc


# PREROUTING for download traffic

#
# HELP
#
# only works with PREROUTING or INPUT but then tc doesn't seem to use the marks!
#
#
#
iptables -I PREROUTING -d ${lan_ip} -t mangle -j MARK --set-mark 13 # 0xd


# ssh, webinterfaces: todo, but that's not so hard