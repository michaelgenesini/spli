import os
import sys

from utils import charToBin

class Occurrence:

	def __init__ (self, file):
		# storing file and key/mode to decode file
		self.file = file
		self.exclude = ['\n','\t',' ']
		self.len = 0
		self.obj = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}

	def occurrence(self):
		with open(self.file) as source:
			text = source.read()
		text.strip()
		for c in text:
			c = c.lower()
			if int(charToBin(c), 2) > 128 or c in self.exclude:
				continue
			self.obj[c]+=1
			self.len+=1
		ordin = []
		for k, o in self.obj.items():
			self.obj[k] = (round(((float(o)/self.len)*100),3))
			ordin.append((k,self.obj[k]))
		ordin.sort(key=lambda o:o[1], reverse=True)
		out = open('files/frequency_crypted.txt', 'wb')
		out.write("".join(o[0].upper() for o in ordin)+"\n")
		for o in ordin:
			out.write(str(o[1])+"\n")
		out.close()