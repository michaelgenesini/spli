#def bin (s):
#    return str(s) if s<=1 else bin(s>>1) + str(s&1)
import os
import itertools
import operator
import hashlib

MAX = 123 # non sappiamo la matematica zio can
MIN = 97

def charToBin (c):
	s = format(ord(c),'b').zfill(8)
	return s

def get_chunks_from_file(file,len):
	""" get_chunks_from_file (filename, chunk_len) """
	f = open(file, "rb")
	header = f.read(18)
	chunks = []
	chunk = ''
	n = 0
	while(1):
		# read a byte
		byte = f.read(1)
		if not byte:
			if chunk!='':
				chunks.append(chunk)
			break
		chunk = chunk + charToBin(byte)
		n = n + 1
		if n == len//8:
			chunks.append(chunk)
			chunk = ''
			n = 0
	f.close()
	return (header, chunks)

def get_md5(file):
	f = open(file, "rb")
	m = hashlib.md5()
	m.update(f.read())
	f.close()
	return m.hexdigest()

def andStrings (s1,s2):
	""" return a string with and bit a bit """
	#return "".join(ord(x) & ord(y) for x, y in zip(s1, s2))
	o = ''
	for i in xrange(0,len(s1)):
		if s1[i] == '1' and s2[i] == '1':
			o = o + '1'
		else:
			o = o + '0'
	return o

def notString (s):
	""" return a string complementrary to the input one """
	o = ''
	for c in s:
		if c == '1':
			o = o + '0'
		else:
			o = o + '1'
	return o

def xorStrings(s1, s2):
	"""
	Returns XOR result from two string
	"""
	return "".join(str(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def shift_left (s,n):
	string = ''
	for i in range(0, n+1):
		string = s[(i % len(s)):] + s[:(i % len(s))]
	return string

def func (chunk,k):
	# primi 16 bits
	c1 = chunk[:len(chunk)/2]
	# ultimi 16 bits
	c2 = chunk[len(chunk)/2:]
	# F = AND(NOT(c2),K)
	f = xorStrings(shift_left(andStrings(xorStrings(notString(c2),k), k),5),shift_left(k,3))
	# out = XOR(F, c1)
	o = xorStrings(c1,f)
	return c2 + o