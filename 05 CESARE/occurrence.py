import os
import sys

from utils import charToBin

if __name__ == '__main__':

	# checking arguments
	if len(sys.argv) < 1:
		print "BAD USAGE:"
		print "python occurrence.py filename"
		sys.exit(0)

	# selected mode
	f = sys.argv[1]
	exclude = ['\n','\t',' ']
	len = 0
	obj = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
	with open(f) as source:
		text = source.read()
	text.strip()
	for c in text:
		c = c.lower()
		if int(charToBin(c), 2) > 128 or c in exclude:
			continue
		#if not c in exclude:
		obj[c]+=1
		len+=1
	print "Len:", str(len)
	ordin = []
	for k, o in obj.items():
		obj[k] = (round(((float(o)/len)*100),3))
		ordin.append((k,obj[k]))
	ordin.sort(key=lambda o:o[1], reverse=True)
	print "Obj: \n", ordin
	out = open("cesare.txt", "wb")
	out.write("".join(o[0].upper() for o in ordin)+"\n")
	for o in ordin:
		out.write(str(o[1])+"\n")
	out.close()