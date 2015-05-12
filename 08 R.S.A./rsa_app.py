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
	print 'Encoding ...'
	print 'Filename: ',filename
	print 'Len Key: ',lenk
	cmd = ["python3","rsa.py", "encode", filename, lenk]
	print 'TEST: ', cmd
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	out,err = p.communicate()
	title = 'R.S.A.'
	data = {'title': title, 'out': out, 'err': err}
	return data

@app.expose("/decode")
def rsa():
	title = 'R.S.A. Decode'
	data = {'title': title}
	return data

@app.expose("/bruteforce")
def bruteforce():
	title = 'R.S.A. Bruteforce'
	data = {'title': title}
	return data

if __name__ == "__main__":
	app.run()
