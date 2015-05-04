import os
import sys
import random

from utils import *
from decoder import Decoder
from encoder import Encoder

if __name__ == '__main__':

	# checking arguments
	if len(sys.argv) < 3:
		print "BAD USAGE:"
		print "python feistel.py encode filename"
		print "python feistel.py decode filename key"
		sys.exit(0)

	print "Feistel"

	# selected mode
	mode = sys.argv[1]

	# selected filename
	filename = sys.argv[2]

	key_len		= 6
	chunk_len	= 32
	times		= 16

	k = ''
	for i in range(0,key_len):
		k = k + str(random.randrange(0,2))
	# Shared key serve per passarcela a voce tra i due client che vogliono scambiarsi il messaggio
	print "Shared key:\t",k

	# questo è l'md5 del file che eventualmente usiamo per testare se viene lo stesso al decript
	print "File md5:\t", get_md5(filename)

	# check if file exists
	if not os.path.isfile(filename):
		print "ERROR: File doesn't exists."
		sys.exit(0)

	# creating encoder or decoder
	if mode == "encode":
		print "Encoding ..."
		Encoder(filename, chunk_len, k, times).encode()
	elif mode == 'decode':
		#selected key
		key = sys.argv[3]
		print 'Decoding'