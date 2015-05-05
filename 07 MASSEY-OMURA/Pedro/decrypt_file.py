import os
import sys
import string
import math
#from PIL import Image

#NON FUNZIONA ANCORA
#brew install pillow

def decrypt(key,inputfile,outputfile):

	#Prova classica con apertura file binario
	keyfile = open(key,"rb")
	infile = open(inputfile,"rb")
	outfile = open(outputfile,"wb")

	# reading tga content
	content = infile.read()
	header = content[:18]
	body = content[18:]
	
	infile_lenght = len(body)#os.fstat(infile.fileno()).st_size

	padbyte = bytearray(keyfile.read())
	
	#byte = bytearray(infile.read())

	#shiftn = 8-(padbyte[0]%8)
	#shiftn2 = 8-shiftn
	#shiftmask = int(math.pow(2, shiftn2))-1;
	#shiftmask2 = 255 ^ shiftmask
	
	# writing header
	outfile.write(header)
	
	for i in range(0, infile_lenght):
		#byte[i] = byte[i] ^ padbyte[i]		
		#temp = ((byte[i] & shiftmask) << shiftn) | ((byte[i] & shiftmask2) >> shiftn2)
		#byte[i] = temp
		outfile.write(chr(ord(body[i]) ^ padbyte[i]))
	
	keyfile.close()
	infile.close()
	outfile.close()
