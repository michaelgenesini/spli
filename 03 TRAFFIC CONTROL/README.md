# 3: TRAFFIC CONTROL


|	.				|	.		|	.				|
| ---- 				| ---- 		| ---- 				|
|	Router **.10**	|--forward-->|	Internet		|
| 	 				| 	 		| 	 				|
|	Michael **.20**	|	---->	|	Router **.10**	|
|	Enrico **.30**	|	---->	|	Router **.10**	|
|	Marco **.40**	|	---->	|	Router **.10**	|
|	Marcello **.50**|	---->	|	Router **.10**	|
|	Netbook **.60**	|	---->	|	Router **.10**	|

### Test 1
Limitazione banda delle connessioni sulla porta 22
 - Michael: copia di un file da router a locale
```
sudo scp mp@10.10.10.10:/home/mp/copia.jpg /Users/michael/Desktop
```

### Test 2
Limitazione banda di tutte le connessioni di un determinato IP
 - Pedro: prova di connessione http, ssh, scp, mail ...

### Test 3
Corruzione pacchetti
 - Netbook: pinga il router e vede i pacchetti corrotti
```
ping 10.10.10.10
```

### Test 4
Rallentamento di tutti i pacchetti ad un determinato IP
 - Marco: pinga il router e vede i pacchetti di reply ritardati oppure ssh verso server vede un ritardo nel typing
```
ping 10.10.10.10
```

### Test 5
Limitazione banda sulla porta 80
 - Marcello: tenta una connessione HTTP(80) e una HTTPS(443)
```
wget http://releases.ubuntu.com/14.04.2/ubuntu-14.04.2-desktop-amd64.iso
```
---