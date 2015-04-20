from utils import *
from occurrence import Occurrence
from decoder import Decoder

import traceback

class Frequency:

	def __init__ (self, file):
		# storing file and key/mode to decode file
		self.file = file
		self.origin = open('frequency_eng.txt', 'rb')
		self.freq_origin = []
		self.freq_crypted = []
		self.keys = []

	def frequency (self):
		'''
			frequency
				1: chiama occurrence passandogli il file criptato
					occurrence cicla tutto il file e conta le occorrenze di ogni lettera,
					crea un file di output 'frequency_crypted.txt' ordinato per frequenze decrescenti
				2: apre il file creato da occurrence e prende le prime X
		'''
		Occurrence(self.file).occurrence()
		f = open('files/frequency_crypted.txt', 'rb')
		for i in range(0,26):
			self.freq_origin.append(int(charToBin(self.origin.read(1)), 2))
			self.freq_crypted.append(int(charToBin(f.read(1)), 2))
		print 'Origin Frequency', self.freq_origin
		print 'Crypted Frequency', self.freq_crypted
		for i in range(0,26):
			self.keys.append(findKey(self.freq_crypted[i], self.freq_origin[i]))
		print 'Keys from Frequency', self.keys
		k = most_common(self.keys)
		print 'MOST COMMON KEY:' + str(k)
		Decoder(self.file, k).decode()

