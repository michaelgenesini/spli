import os
import sys
import string
import math

def encrypt(key,inputfile,outputfile):

	#Prova classica con apertura file binario
	keyfile = open(key,"wb")
	infile = open(inputfile,"rb")
	outfile = open(outputfile,"wb")

	# reading tga content
	content = infile.read()
	header = content[:18]
	body = content[18:]

	# generating random key
	randomGen = open('/dev/urandom','rb')
	infile_lenght = len(body)#os.fstat(infile.fileno()).st_size
	pad = randomGen.read(infile_lenght)
	keyfile.write(pad)
	keyfile.close()
	randomGen.close()
	
	# creating padbyte for encription
	padbyte = bytearray(pad)
	
	#byte = bytearray(infile.read())

	#shiftn = padbyte[0]%8
	#shiftn2 = 8-shiftn
	#shiftmask = int(math.pow(2, shiftn2))-1;
	#shiftmask2 = 255 ^ shiftmask

	# writing header
	outfile.write(header)
	
	for i in range(0, infile_lenght):
		#temp = ((byte[i] & shiftmask) << shiftn) | ((byte[i] & shiftmask2) >> shiftn2)
		#byte[i] = temp
		outfile.write(chr(ord(body[i]) ^ padbyte[i]))

	infile.close()
	outfile.close()


	#Lo stesso problema c'e se hai 255 e sommi va in crisi
