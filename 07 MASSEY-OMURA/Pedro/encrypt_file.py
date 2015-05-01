import os
import sys
import string
import math
#from PIL import Image

#NON FUNZIONA ANCORA
#brew install pillow

def encrypt(key,inputfile,outputfile):

	#im = Image.open(inputfile,"r")


	#Prende i soli dati di un'immagine
	#prova = list(im.getdata())

	#print prova[0]

	#converte lista di triplette in lista di elementi singoli
	#res = [i[0] for i in prova] 

	#converte lista in array di interi
	#inpixel = []
	#inpixel = [int(pix) for pix in res]


	#Ora dovrei aggiungere la chiave ad ogni dato 
	#i=0
	#for element in inpixel:
	#	element = element << key
	#	print element,"\n"

	#print inpixel[0]
	#Dopo aver ricreato una lista di triplette basta fare il contrario:

	#im2.putdata() e riesci a creare l'immagine con i pixel shiftati		


	#Prova classica con apertura file binario
	keyfile = open(key,"wb")
	infile = open(inputfile,"rb")
	outfile = open(outputfile,"wb")

	randomGen = open('/dev/urandom','rb')
	infile_lenght = os.fstat(infile.fileno()).st_size
	pad = randomGen.read(infile_lenght)
	keyfile.write(pad)
	keyfile.close()
	
	padbyte = bytearray(pad)
	
	byte = bytearray(infile.read())

	shiftn = padbyte[0]%8
	shiftn2 = 8-shiftn
	shiftmask = int(math.pow(2, shiftn2))-1;
	shiftmask2 = 255 ^ shiftmask
	
	for i in range(0, infile_lenght):
		#temp = ((byte[i] & shiftmask) << shiftn) | ((byte[i] & shiftmask2) >> shiftn2)
		#byte[i] = temp
		outfile.write(chr(byte[i] ^ padbyte[i]))
	
	infile.close()
	outfile.close()


	#Lo stesso problema c'e se hai 255 e sommi va in crisi
