from utils import *

import traceback

class Encoder:

	def __init__ (self, file, chunk_len, k, times):
		# storing file and key to encode
		self.file = file
		self.k = k.ljust(chunk_len/2, '0') 
		print 'k: \t\t',self.k
		self.chunk_len = chunk_len
		self.times = times
		self.chunks = get_chunks_from_file(file,chunk_len)
		if len(self.chunks)<32:
			print 'Devo completare l\'ultimo'
			print self.chunks[len(self.chunks)-1]
		# storing output file destination
		#self.output = file.split(".")[0] + "_encoded." + file.split(".")[1]

	def encode (self):
		print "Encoding"
		encoded_chunks = []
		print 'chunks:\t\t',self.chunks
		for chunk in self.chunks:
			for i in range(0,self.times):
				chunk = self.func(chunk,self.k)
			encoded_chunks.append(chunk)
		print '\nencoded_chunks:\t',encoded_chunks

	def func (self,chunk,k):
		# ultimi 16 bits
		c1 = chunk[:len(chunk)/2]
		# primi 16 bits
		c2 = chunk[len(chunk)/2:]
		# F = AND(NOT(c2),K)
		f = andStrings(notString(c2),k)
		# out = XOR(F, c1)
		o = xorStrings(f,c1)
		# decommentare queste print per vedere il funzionamento dell funzione
		#print '-------------------CHUNK'
		#print 'chunk:\t\t',c2
		#print '-------------------'
		#print 'not:\t\t',notString(c2)
		#print 'k:\t\t',k
		#print '-------------------'
		#print 'F:\t\t',f
		#print 'chunk:\t\t',c1
		#print '-------------------'
		#print 'xor:\t\t', o
		#print 'new chunk: \t', c2 + o
		return c2 + o
