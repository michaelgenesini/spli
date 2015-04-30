import os
import sys
import string
from PIL import Image

#NON FUNZIONA ANCORA
#brew install pillow

def encrypt(key,inputfile,outputfile):

	im = Image.open(inputfile,"r")


	#Prende i soli dati di un'immagine
	prova = list(im.getdata())

	print prova[0]

	#converte lista di triplette in lista di elementi singoli
	res = [i[0] for i in prova] 

	#converte lista in array di interi
	inpixel = []
	inpixel = [int(pix) for pix in res]


	#Ora dovrei aggiungere la chiave ad ogni dato 
	i=0
	for element in inpixel:
		element += key
		#print element,"\n"


	#Dopo aver ricreato una lista di triplette basta fare il contrario:

	#im2.putdata() e riesci a creare l'immagine con i pixel shiftati		


	

		





	