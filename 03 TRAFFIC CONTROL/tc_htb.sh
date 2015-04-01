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

#iptables -A PREROUTING -i $INTIF -t mangle -s $pedro -j MARK --set-mark 50
#iptables -A OUTPUT -i $INTIF -t mangle -s $pedro -p tcp --sport 80 -j MARK --set-mark 40
#iptables -A OUTPUT -i $INTIF -t mangle -p tcp --sport 22 -j MARK --set-mark 30

#Cancella regole traffic control
tc qdisc del dev $INTIF root


#Crea l'albero con infiniti figli e di conseguenza infinite regole di controllo (root è radice albero non c'entra con i permessi )
tc qdisc add dev $INTIF handle 1: root htb

#La classe root non ha nessuna regola che gli limita il traffico (gli do 1000MB/s)
tc class add dev $INTIF parent 1: classid 1:1 htb rate 1000Mbps

#Creo i figli specificando il padre e ad ognuno associo una bit-rate non limitante
tc class add dev $INTIF parent 1:1 classid 1:11 htb rate 100Mbps
tc class add dev $INTIF parent 1:1 classid 1:12 htb rate 100Mbps
tc class add dev $INTIF parent 1:1 classid 1:13 htb rate 100Mbps
tc class add dev $INTIF parent 1:1 classid 1:14 htb rate 100Mbps prio 1
tc class add dev $INTIF parent 1:1 classid 1:15 htb rate 100Mbps prio 0

#Arrivato qui ho due modi per applicare le regole (perdita, delay, bit-rate associata ecc..) NETEM O TBF:

tc qdisc add dev $INTIF parent 1:11 handle 10: netem delay 100ms 10ms
tc qdisc add dev $INTIF parent 1:12 handle 20: netem loss 50%
tc qdisc add dev $INTIF parent 1:13 handle 60: tbf rate 20kbps buffer 1600 limit 3000
tc qdisc add dev $INTIF parent 1:14 handle 61: tbf rate 30kbps buffer 1600 limit 3000
tc qdisc add dev $INTIF parent 1:15 handle 62: tbf rate 40kbps buffer 1600 limit 3000

#Filtro su IP alla porta 80 HTTP
#tc filter add dev $INTIF parent 1:0 prio 1 protocol ip handle 40 fw flowid 1:14

#Filtro su porta 22 SSH
#tc filter add dev $INTIF parent 1:0 prio 0 protocol ip handle 30 fw flowid 1:15

#Filtro su un IP destinatario per loss
#tc filter add dev $INTIF protocol ip parent 1:0 prio 3 u32 match ip dst $pedro flowid 1:12

#Filtro su un IP destinatario per il delay
#tc filter add dev $INTIF protocol ip parent 1:0 prio 3 u32 match ip dst $pedro flowid 1:11

#Filtro con mangle e mark per tbf
#tc filter add dev $INTIF protocol ip parent 1:0 prio 1 u32 match ip dst $pedro flowid 1:13
#tc filter add dev $INTIF parent 1: protocol ip handle 50 fw flowid 1:13

#Filtro su una porta specifica (non usato al momento) 
#tc filter add dev $INTIF protocol ip prio 1 u32 match ip dport 5001 0xffff flowid 1:13


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

