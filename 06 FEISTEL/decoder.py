from utils import *

import traceback

class Decoder:

	def __init__ (self, file, chunk_len, k, times):
		# storing file and key to encode
		self.file = file
		# ljust(len,'') completa la chiave con zeri alla fine per renderla lunga come il mezzo chunk (16)
		self.k = k.ljust(chunk_len/2, '0') 
		
		self.chunk_len = chunk_len
		self.times = times
		self.header, self.chunks = get_chunks_from_file(file,chunk_len)

		if len(self.chunks[len(self.chunks)-1])<chunk_len:
			#print 'Devo completare l\'ultimo'
			self.chunks[len(self.chunks)-1] = self.chunks[len(self.chunks)-1].zfill(32)
			print "creating output file ..."
		# storing output file destination
		self.output = file.split(".")[0] + "_decoded." + file.split(".")[1]

	def decode (self):
		decoded_chunks = []
		for chunk in self.chunks:
			for i in range(0,self.times):
				chunk = func(chunk,self.k)
			decoded_chunks.append(chunk[16:32]+chunk[0:16])
		out = open(self.output, "wb")
		out.write(self.header)
		for i in decoded_chunks:
			out.write(chr(int(i[0:8],2)))
			out.write(chr(int(i[8:16],2)))
			out.write(chr(int(i[16:24],2)))
			out.write(chr(int(i[24:32],2)))
		out.close()
		print 'MD5 Decryted:\t', get_md5(self.output)