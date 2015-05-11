from weppy import App
from client import Client

app = App(__name__)

@app.expose("/")
def index():
	title = 'R.S.A.'
	data = {'title': title}
	return data

@app.expose("/encode/<str:filename>/<int:len>")
def rsa(filename,len):
	title = 'R.S.A.'
	print 'Encoding ...'
	print 'Filename: ',filename
	print 'Len Key: ',len
	e = Client(filename, len)
	e.encode(e.pubkey)
	e.decode(e.C)
	data = {'title': title, 'p': e.p, 'q': e.q, 'n': e.n}
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
