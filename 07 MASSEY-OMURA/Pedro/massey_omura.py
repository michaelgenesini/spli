import sys, os, string
from encrypt_file import encrypt
from decrypt_file import decrypt

#Main del progetto

#Struttura:
#python cesare.py -e:d key inputfile outputfile
#e cripta d decripta

#Controllo argomenti e a seconda del flag che viene chiamato (e o d)
#chiama rispettivamente la funzione encrypt o decrypt

#Controllo argomenti
args = len(sys.argv)
usage = "Usage: python massey_omura.py [inputfile] [outputfile] [-de] [key]"

inputfile = sys.argv[1]
outputfile = sys.argv[2]

decrypting = False
if (args < 4):
	print "Error: few arguments\n",usage
	sys.exit(1)

if(sys.argv[3] == '-d'):
	decrypting = True

#Passo la chiave come nome di file. La chiave verra generata e utilizzata in encrypt e poi utilizzata in decrypt
key = sys.argv[4]		

checkfile1 = os.path.isfile(inputfile)
checkfile2 = os.path.isfile(key)

if ((decrypting) and (checkfile2 == False)):
	print "Error: file doesn't exists -> ",sys.argv[4], "\n",usage
	sys.exit(2)

if (checkfile1 == False):
	print "Error: file doesn't exists -> ",sys.argv[1], "\n",usage
	sys.exit(3)
############################################################################


#Chiama funzione encrypt o decrypt a seconda del flag e esce

if(not(decrypting)):
	encrypt(key,inputfile,outputfile)

elif(decrypting):
	decrypt(key,inputfile,outputfile)
else:
	sys.exit(69)






