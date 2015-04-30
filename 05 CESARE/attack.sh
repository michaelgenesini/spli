#!/bin/bash

# tcpdump -w /Users/michael/Desktop/dump.pcap
# tshark -r /Users/michael/Desktop/dump.pcap -V > /Users/michael/Desktop/converted.txt

#Attacco Automatico
#ssh da fare manualmente
#ssh michael@10.10.10.10:~/Documents/spli/05\ Cesare/
#./run.sh
#scp michael@10.10.10.10:"~/Documents/spli/05\ Cesare/log.txt" "/Users/Marci/Box Sync/Università/Sicurezza Progettazione Laboratorio Internet/Progetto/05 CESARE/files/log.txt"

cd /Users/Marci/spli/05\ CESARE/files 
sed -n "/START_WS/,/END_WS/p" log.txt > clean.txt
echo `cat clean.txt | tr -d ":"` > clean.txt 
echo `cat clean.txt | tr -d "/"` > clean.txt 
echo `cat clean.txt | tr -d "~"` > clean.txt 
echo `cat clean.txt | tr -d "*"` > clean.txt 
echo `cat clean.txt | tr -d '\'` > clean.txt 

cd ..
echo $PWD
python caesar.py occurrence files/clean.txt

cd Cesare\ Octave
echo $PWD
octave --persist Cesare.m

cd ..
python caesar.py freq files/clean.txt

cat files/clean_decoded.txt
