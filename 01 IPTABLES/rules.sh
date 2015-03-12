#!/bin/bash
#
#	Michael Iptables Rules
#

echo 'Ciao Bel'

stagni 	=		10.42.0.34
marci 	=		10.42.0.54
pedro 	=		10.42.0.1
mike 	=		10.42.0.51

router 	=		$pedro

iptables -F
iptables -X
iptables -Z
iptables -t nat -F

iptables -t nat -P PREROUTING ACCEPT

 
# 10.10.10.X pinga 10.10.10.139
# 10.10.10.X vede che il ping e tra lui e 10.10.10.214
#
#iptables -t nat -A PREROUTING -d 10.10.10.139 -j DNAT --to-destination 10.10.10.214
#iptables -t nat -A PREROUTING -p TCP --dport 80 -d 10.10.10.139 -j DNAT --to-destination 10.10.10.214:80

 
# 10.10.10.139 pinga 10.10.10.X
# 10.10.10.X vede che sta pingando con 10.10.10.214
#
# se 10.10.10.139 pinga 10.10.10.214
# 10.10.10.214 vede che pinga con se stesso
#iptables -t nat -A POSTROUTING -s 10.10.10.139 -j SNAT --to-source 10.10.10.214
#iptables -t nat -A POSTROUTING -p TCP --dport 70 -d 10.10.10.139 -j SNAT --to-destination 10.10.10.214

#
# Droppo tutto tranne quello che arriva da 10.10.10.140
#
iptables -P INPUT DROP
iptables -A INPUT -s 10.10.10.140 -j ACCEPT
