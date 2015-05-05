from utils import *

import traceback

class Encoder:

	def __init__ (self, file, chunk_len, k, times):
		# storing file and key to encode
		self.file = file
		# ljust(len,'') completa la chiave con zeri alla fine per renderla lunga come il mezzo chunk (16)
		self.k = k.ljust(chunk_len/2, '0') 
		self.chunk_len = chunk_len
		self.times = times
		self.chunks = get_chunks_from_file(file,chunk_len)
		
		if len(self.chunks[len(self.chunks)-1])<chunk_len:
			print 'Devo completare l\'ultimo'
			print 'ultimo ',self.chunks[len(self.chunks)-1]
			self.chunks[len(self.chunks)-1] = self.chunks[len(self.chunks)-1].zfill(32)
			print 'ultimo ',self.chunks[len(self.chunks)-1]
		# storing output file destination
		self.output = file.split(".")[0] + "_encoded." + file.split(".")[1]

	def encode (self):
		encoded_chunks = []
		print 'MD5 Origin:\t', get_md5(self.file)
		for chunk in self.chunks:
			for i in range(0,self.times):
				chunk = func(chunk,self.k)
			encoded_chunks.append(chunk[16:32]+chunk[0:16])
		out = open(self.output, "wb")
		for i in encoded_chunks:
			out.write(chr(int(i[0:8],2)))
			out.write(chr(int(i[8:16],2)))
			out.write(chr(int(i[16:24],2)))
			out.write(chr(int(i[24:32],2)))
		out.close()