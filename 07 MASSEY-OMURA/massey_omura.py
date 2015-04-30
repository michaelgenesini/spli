import sys, os, string
from encrypt_file import encrypt
#from decrypt_file import decrypt

#Main del progetto

#Struttura:
#python cesare.py -e:d key inputfile outputfile
#e cripta d decripta

#Controllo argomenti e a seconda del flag che viene chiamato (e o d)
#chiama rispettivamente la funzione encrypt o decrypt

#Controllo argomenti
args = len(sys.argv)
usage = "Usage: python massey_omura.py [-de] key [inputfile] [outputfile]"

flag = sys.argv[1]
key = sys.argv[2]
inputfile = sys.argv[3]
outputfile = sys.argv[4]

if (args != 5):
	print "Error: few arguments\n",usage
	sys.exit(1)

if (flag != '-e' and flag != '-d'):
	print "Error: unexpected second argument -> ",flag, "\n",usage
	sys.exit(2)

try:
    x = int(key)
except ValueError:
	print "Error: key is not a number -> ",key, "\n",usage
	sys.exit(3)

checkfile1 = os.path.isfile(inputfile)


if (checkfile1 == False):
	print "Error: file doesn't exists -> ",sys.argv[3], "\n",usage
	sys.exit(4)
############################################################################


#Chiama funzione encrypt o decrypt a seconda del flag e esce

k = int(key)
if(flag == '-e'):
	encrypt(k,inputfile,outputfile)

elif(flag == '-d'):
	decrypt(k,inputfile,outputfile)
else:
	sys.exit(69)






