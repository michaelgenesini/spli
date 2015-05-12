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
	out, err = encode(filename,lenk)
	title = 'R.S.A.'
	data = {'title': title, 'filename': filename, 'out': [s.strip() for s in out.splitlines()], 'err': err}
	return data

@app.expose("/bruteforce/<str:filename>/<int:lenk>")
def bruteforce(filename,lenk):
	title = 'R.S.A. Bruteforce'
	data = {'title': title}
	return data

def encode(filename, lenk):
	pathtofile = "static/imgs/"+filename
	print pathtofile
	cmd = ["python3","rsa.py", "encode", pathtofile, lenk]
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	out,err = p.communicate()
	return (out, err)

if __name__ == "__main__":
	app.run()