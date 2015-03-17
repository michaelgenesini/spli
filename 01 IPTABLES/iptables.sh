#!/bin/bash
#
#	Iptables Rules
#

echo 'Ciao Bel'

default="10.10.10."
mike=$default"20"
marco=$default"30"
marci=$default"Y"
pedro=$default"Z"
router=$default"10"

mikeMac="54:26:96:db:a4:ad"

trusted=""

# External Public Interface
EXTIF="eth0"

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

# SISTEMARE IP
#
# Nella rete interna tutte le chiamate sulla porta 80 al router vengono
# ridirezionate sulla porta 8000 a Marco che ha un servizio che deve essere
# accessibile a tutta la rete interna
#
iptables -t nat -A PREROUTING -i $INTIF -p tcp --dport 80 -d $router -s $INTIPS -j DNAT --to-destination $marco:8000


# 10.10.10.139 pinga 10.10.10.X
# 10.10.10.X vede che sta pingando con 10.10.10.214
#
# se 10.10.10.139 pinga 10.10.10.214
# 10.10.10.214 vede che pinga con se stesso
#iptables -t nat -A POSTROUTING -s 10.10.10.11 -j SNAT --to-source 10.10.10.9

#
# Droppo tutto tranne quello che arriva da 10.10.10.140
#
#iptables -P INPUT DROP
#iptables -A INPUT -s 10.10.10.9 -j ACCEPT
#

#iptables -A OUTPUT -p tcp -d "www.facebook.com" -j DROP

iptables -A INPUT -i $INTIF -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i $EXTIF -p tcp --dport 22 -m mac --mac-source $mikeMac -j ACCEPT
iptables -A OUTPUT -o $INTIF -p tcp --dport 22 -m state --state ESTABLISHED -j ACCEPT

iptables -A FORWARD -i $INTIF -o $EXTIF -j ACCEPT

iptables -t nat -A POSTROUTING -s $INTIPS -j MASQUERADE
