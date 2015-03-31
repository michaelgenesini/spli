#!/bin/bash
#
# Iptables Rules
#
echo 'Ciao Bel'
echo "*****************************"
default="10.10.10."
mike=$default"20"
marco=$default"40"
marci=$default"50"
pedro=$default"30"
router=$default"10"
# External Public Interface
EXTIF="usb0"
# Internal Private Interface
INTIF="wlan0"
# Internal IPs
INTIPS=$default"0/24"
iptables -F
iptables -X
iptables -Z
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -t nat -P PREROUTING ACCEPT
iptables -t nat -P POSTROUTING ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT


iptables -A FORWARD -i $INTIF -o $EXTIF -j ACCEPT

iptables -t nat -A POSTROUTING -s $INTIPS -j MASQUERADE

#Cancella regole traffic control
tc qdisc del dev wlan0 root


#Delay e loss da vedere con ping verso il rooter
#tc qdisc add dev wlan0 root netem delay 200ms 20ms distribution normal
#
#tc qdisc add dev wlan0 root netem loss 0.5%


#Mangle
iptables -A PREROUTING -i wlan0 -t mangle -s $pedro -j MARK --set-mark 5
iptables -A PREROUTING -i wlan0 -t mangle -s $marci -j MARK --set-mark 6


#TC creo padre
tc qdisc add dev wlan0 root handle 1:0 htb

#TC Class
tc class add dev wlan0 parent 1:0 classid 1:5 htb rate 20kbps ceil 30kbps
tc class add dev wlan0 parent 1:0 classid 1:6 htb rate 60kbps ceil 90kbps

#TC Filtro
tc filter add dev wlan0 parent 1:0 protocol ip handle 5 fw flowid 1:5
tc filter add dev wlan0 parent 1:0 protocol ip handle 6 fw flowid 1:6

#Stampa regole tc
echo "Regole Iptables:"
iptables -t mangle -L
echo "*****************************"
echo "Regole TC:"
tc qdisc ls dev wlan0
tc class ls dev wlan0
tc filter ls dev wlan0
echo "*****************************"

