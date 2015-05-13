from weppy import App
from client import Client
import subprocess

app = App(__name__)

@app.expose("/")
def index():
	title = 'R.S.A.'
	data = {'title': title}
	return data

@app.expose("/encode/<str:filename>/<int:lenk>")
def rsa(filename,lenk):
	title = 'R.S.A.'
	temp = open("temp", "wb")
	temp.write(filename)
	temp.write('\n')
	temp.write(str(lenk))
	temp.close()
	out, err = encode(filename,lenk)
	title = 'R.S.A.'
	data = {'title': title, 'filename': filename, 'out': [s.strip() for s in out.splitlines()], 'err': [s.strip() for s in err.splitlines()]}
	return data

@app.expose("/bruteforce")
def bruteforce():
	title = 'R.S.A. Bruteforce'
	temp = open("temp","rb")
	f = temp.readline()
	l = temp.readline()
	temp.close()
	out, err = bruteforce(f,l)
	data = {'title': title, 'out': [s.strip() for s in out.splitlines()], 'err': [s.strip() for s in err.splitlines()]}
	return data

def encode(filename, lenk):
	pathtofile = "static/imgs/"+filename
	print pathtofile
	cmd = ["python3","rsa.py", "encode", pathtofile, lenk]
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	out,err = p.communicate()
	return (out, err)

def bruteforce(filename, lenk):
	pathtofile = "static/imgs/"+filename
	print pathtofile.splitlines()[0]
	cmd = ["python3","rsa.py", "bruteforce", pathtofile.splitlines()[0], str(lenk)]
	print cmd
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	out,err = p.communicate()
	return (out, err)

if __name__ == "__main__":
	app.run()