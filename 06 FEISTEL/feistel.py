import os
import sys
import random

from utils import *
from decoder import Decoder
from encoder import Encoder
from bruteforce import Bruteforce

if __name__ == '__main__':

	# checking arguments
	if len(sys.argv) < 3:
		print "BAD USAGE:"
		print "python feistel.py encode filename"
		print "python feistel.py decode filename key"
		print "python feistel.py bruteforce filename md5"
		sys.exit(0)

	print "Feistel"

	# selected mode
	mode = sys.argv[1]

	# selected filename
	filename = sys.argv[2]

	key_len		= 16
	chunk_len	= 32
	times		= 16 #16

	# check if file exists
	if not os.path.isfile(filename):
		print "ERROR: File doesn't exists."
		sys.exit(0)

	# creating encoder or decoder
	if mode == 'encode':
		k = ''
		for i in range(0,key_len):
			k = k + str(random.randrange(0,2))
		# Shared key serve per passarcela a voce tra i due client che vogliono scambiarsi il messaggio
		print "Shared key:\t",k
		print 'Encoding ...'
		Encoder(filename, chunk_len, k, times).encode()
	elif mode == 'decode':
		if len(sys.argv) < 4:
			print "python feistel.py decode filename key"
			sys.exit(0)
		#selected key
		key = sys.argv[3]
		print 'Decoding ...'
		Decoder(filename, chunk_len, key, times).decode()
	elif mode == 'bruteforce':
		if len(sys.argv) < 4:
			print "python feistel.py bruteforce filename md5"
			sys.exit(0)
		#selected key
		md5 = sys.argv[3]
		Bruteforce(filename, chunk_len,key_len, md5, times).guess()
