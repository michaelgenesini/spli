#!/bin/bash

#bytes=`wc -c file.jpg` #mi da il numero di byte del file

#tcpdump -n -i en0 -s bytes #legge tot bytes di un pacchetto
#				  -X #mostra dati pacchetto senza header
#				  -q #mostra meno informazioni sul protocollo


HOST='10.10.10.10'
USER='marcoponds'
PASSWD='pèàòlo'
FILE='Lena.xbm'

ftp -n -v $HOST << EOT
quote USER $USER
quote PASS $PASSWD
pwd
get $FILE
quit
EOT
exit 0
