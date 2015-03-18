#!/bin/bash
#
#	Iptables Rules
#

echo 'Ciao Bel'

default="10.10.10."
mike=$default"20"
marco=$default"40"
marci=$default"50"
pedro=$default"30"
router=$default"10"
mikeMac="54:26:96:db:a4:ad"
openPorts="80,443,9091"
mailPorts="143,993,110,995,25"

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
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD ACCEPT

iptables -A FORWARD -i $INTIF -o $EXTIF -j ACCEPT

#
# Nella rete interna tutte le chiamate sulla porta 80 al router vengono
# ridirezionate sulla porta 8000 a Marco che ha un servizio che deve essere
# accessibile a tutta la rete interna
#
iptables -t nat -A PREROUTING -i $INTIF -p tcp --dport 80 -d $router -s $INTIPS -j DNAT --to-destination $marco:8000
iptables -t nat -A PREROUTING -i $INTIF -p tcp -m multiport --dports $openPorts",22,"$mailPorts -j ACCEPT

#
# Blocca degli specifici indirizzi IP oppure host
#
#iptables -A OUTPUT -d www.facebook.com -j DROP
#iptables -A OUTPUT -d facebook.com -j REJECT

#
# Consente ssh da dentro la rete per tutti
# Consente ssh da fuori solo ad uno specifico indirizzo MAC
#
iptables -A INPUT -i $INTIF -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i $EXTIF -p tcp --dport 22 -m mac --mac-source $mikeMac -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $INTIF -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

iptables -A INPUT -i $INTIF -p icmp -j ACCEPT
#
# Consente traffico MAIL
# Consente IMAP/IMAP2, IMAPS, POP3, POP3S
#
iptables -A INPUT -i $INTIF -p tcp -m multiport --dports $mailPorts","$openPorts -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o $INTIF -p tcp -m multiport --sports $mailPorts","$openPorts -m state --state ESTABLISHED -j ACCEPT

#
#
#
iptables -A OUTPUT -o $INTIF -p tcp -m multiport --dports $mailPorts","$openPorts -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i $INTIF -p tcp -m multiport --sports $mailPorts","$openPorts -m state --state ESTABLISHED -j ACCEPT


#
# Forward interfaccia da interna a esterna
#
#iptables -A FORWARD -i $INTIF -o $EXTIF -j ACCEPT

iptables -A INPUT -p udp -i $INTIF --sport 53 -j ACCEPT
iptables -A OUTPUT -p udp -o $INTIF --dport 53 -j ACCEPT

iptables -A OUTPUT -o $INTIF -p icmp -j ACCEPT
#iptables -A FORWARD -d facebook.com -j REJECT


iptables -t nat -A POSTROUTING -s $INTIPS -j MASQUERADE

#
#
# LOG
iptables -N LOGGING
iptables -A INPUT -j LOGGING
iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "iptables Packet Dropped: " --log-level 7
iptables -A LOGGING -j DROP
