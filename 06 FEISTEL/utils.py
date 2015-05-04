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

def inc(value, inc, max):
	if ( value + inc ) <= max:
		return value + inc
	return value + inc - max

def dec(value, dec, min):
	if ( value - dec ) >= min:
		return value - dec
	return MAX - MIN + (value - dec)

def findKey(crypted, origin):
	if (crypted - origin) >= 0:
		return crypted - origin
	return MAX - MIN + crypted - origin

def get_chunks_from_file(file,len):
	""" get_chunks_from_file (filename, chunk_len) """
	f = open(file, "rb")
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
	return chunks

def get_md5(file):
	f = open(file, "rb")
	m = hashlib.md5()
	m.update(f.read())
	f.close()
	return m.hexdigest()

def andStrings (s1,s2):
	""" return a string with and bit a bit """
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

def xorStrings (s1,s2):
	""" return a string with xor bit a bit """
	o = ''
	for i in xrange(0,len(s1)):
		if (s1[i] == '1' and s2[i] == '1') or (s1[i] == '0' and s2[i] == '0'):
			o = o + '0'
		else:
			o = o + '1'
	return o