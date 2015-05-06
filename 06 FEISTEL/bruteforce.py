from utils import *
import itertools

import traceback

class Bruteforce:

	def __init__ (self, file, chunk_len, key_len, md5, times):
		self.file = file
		self.key_len = key_len
		self.md5 = md5

		keys_list = list(itertools.product([0,1], repeat=key_len))
		keys = []
		self.keys = []
		for k in keys_list:
			temp = ''
			for i in k:
				temp = temp + str(i)
			keys.append(temp.ljust(chunk_len/2, '0'))

		self.keys = []
		for i in keys:
			temp = generate_keys(i.ljust(chunk_len/2, '0'),times)
			k = []
			for i in reversed(temp):
				k.append(i)
			self.keys.append(k)

		print self.keys

		self.chunk_len = chunk_len
		self.times = times
		self.header, self.chunks = get_chunks_from_file(file,chunk_len)

		if len(self.chunks[len(self.chunks)-1])<chunk_len:
			print 'Devo completare l\'ultimo'
			#print 'ultimo ',self.chunks[len(self.chunks)-1]
			self.chunks[len(self.chunks)-1] = self.chunks[len(self.chunks)-1].zfill(32)
			#print 'ultimo ',self.chunks[len(self.chunks)-1]

	def guess (self):
		n = 0
		for k in self.keys:
			decoded_chunks = []
			print 'PROVA chiave: ', k
			output = self.file.split(".")[0] + "_decoded_" + str(n) + "." + self.file.split(".")[1]
			for chunk in self.chunks:
				for i in range(0,self.times):
										chunk = func(chunk,k[i])
				decoded_chunks.append(chunk[16:32]+chunk[0:16])
			out = open(output, "wb")
			out.write(self.header)
			for i in decoded_chunks:
				out.write(chr(int(i[0:8],2)))
				out.write(chr(int(i[8:16],2)))
				out.write(chr(int(i[16:24],2)))
				out.write(chr(int(i[24:32],2)))
			out.close()
			n += 1
			if get_md5_file(output) == self.md5:
				print "TROVATO! chiave: ", k
				break
			else:
				os.remove(output)
				print 'Provo con una nuova key ...'
