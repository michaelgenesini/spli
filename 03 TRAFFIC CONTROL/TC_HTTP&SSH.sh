#!/bin/bash
#
# Iptables Rules
#

#Abilita Forward su tutte interfacce
sudo sysctl -w net.ipv4.conf.all.forwarding=1



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
INTIF="wlan1"
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
tc qdisc del dev $INTIF root
tc qdisc del dev $EXTIF root


#TC creo padre
tc qdisc add dev $INTIF root handle 1: htb

#TC Class
tc class add dev $INTIF parent 1: classid 1:1 htb rate 1024kbps 
tc class add dev $INTIF parent 1: classid 1:5 htb rate 100kbps ceil 250kbps prio 1
tc class add dev $INTIF parent 1: classid 1:6 htb rate 20kbps ceil 80kbps prio 0

#TC Filtro
tc filter add dev $INTIF parent 1:0 prio 1 protocol ip handle 5 fw flowid 1:5
tc filter add dev $INTIF parent 1:0 prio 0 protocol ip handle 6 fw flowid 1:6

#Mangle in Output
iptables -A OUTPUT -t mangle -s 10.10.10.50 -p tcp --sport 80 -j MARK --set-mark 5
iptables -A OUTPUT -t mangle  -p tcp --sport 22 -j MARK --set-mark 6

#Stampa regole tc
echo "Regole Iptables:"
iptables -t mangle -L
echo "*****************************"
echo "Regole TC:"
tc qdisc ls dev $INTIF
tc class ls dev $INTIF
tc filter ls dev $INTIF
echo "*****************************"

#Per testare la restrizione su http usa wget su una di queste iso che trovi a questo indirizzo
#http://cdimage.ubuntu.com/lubuntu/releases/14.04/release/ 

#Per testare la restrizione su ssh supponendo di copiare un file presente sul pc che fa da router
#e copiarlo in locale dare questo tipo di comando
#sudo scp username_router@10.10.10.10:path_assoluto_file_sul_router path_assoluto_cartella locale