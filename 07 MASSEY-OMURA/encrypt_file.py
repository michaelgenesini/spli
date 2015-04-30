import os
import sys
import string
from PIL import Image

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
	infile = open(inputfile,"rb")
	outfile = open(outputfile,"wb")

	byte = bytearray(infile.read())

	print "prima byte0 =", byte[0]

	byte[0] = byte[0] << 3

	print "Dopo byte0 =", byte[0]

	#Lo stesso problema c'è se hai 255 e sommi va in crisi