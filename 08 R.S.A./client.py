from utils import *
#from bitarray import *
import itertools

class Client:

    def __init__(self, file, numbit):
        '''
            RSA encoding

            - scelta di "p" e "q"
        '''
        print("-------------------- RSA --------------------")
        print(" p = prime number")
        print(" q = prime number")
        print(" n = p * q")
        print(" phi = (p - 1) * (q - 1)")
        print(" e -> 1 < e < phi(n), GCD(e, phi) = 1")
        print(" d -> ")
        print("---------------------------------------------")

        self.md5 = get_md5_file("Lena.tga")
        # storing file
        self.file = file
        # storing info for keys
        self.numbit = int(numbit)
        self.primeLength = int(self.numbit)#/2)
        # creating prime numbers
        try:
            from pyprimes import primes, prime_count

            # creating reference min value and max value
            minValue = int("1".ljust(self.primeLength, "0"))
            maxValue = int("9".ljust(self.primeLength, "9"))

            numprimes = prime_count(maxValue) - prime_count(minValue)
            iterator = primes(minValue, maxValue)
            primesList = [next(iterator) for num in range(0, numprimes)]

            # creatint p and q
            ref = int(round(len(primesList)/3))
            self.p = primesList[ref]
            self.q = primesList[-ref]
            print("P: ", self.p, " Q:", self.q)

            # creating mod and product
            self.chunks = 0
            self.n = self.p * self.q
            self.phi = (self.p-1) * (self.q-1)
            print("N:", self.n, " PHI: ", self.phi)

            for i in range(0,10):
                if pow(256,i)>self.n:
                    self.chunks = i-1
                    break
            print("Chunks: ", self.chunks)

            # choosing e
            flag, self.e = getCoprime(self.phi)
            print("E: ", self.e)

            if flag:
                # choosing d
                self.d = self.getD()
                print("D: ", self.d)

                # salviamo chiave pubblica e privata
                self.pubkey = (self.n, self.e)
                self.privkey = (self.n, self.d)

            self.gotError = False
        except Exception as e:
            print("Yo, missing pyprimes! run 'pip install pyprimes'")
            self.gotError = True
            raise

    def getD(self):
        '''
        val = 1
        while (val*self.e)%self.phi != 1:
            val += 1
        print("about to return D")
        return val
        '''
        return modinv(self.e, self.phi)

    def F(self, file, base, size):
        '''
        converting file to numbers
        '''
        # opening file
        f = open(file, "rb")
        # reading header
        self.header = f.read(18)
        # now only body
        #n = 0
        buffer = []
        byte = f.read(self.chunks)

        while byte:
            if (self.chunks == 1):
                buffer.append(ord(byte))
            else:
                n = 0
                for i in range(0, len(byte)):
                    n = (n << 8) + byte[i]
                buffer.append(n)
            byte = f.read(self.chunks)

        '''
        while byte:
            n = long((n*base) + ord(byte))
            #if n > size:
            if ((n*base) + 255) > self.chunks:
                buffer.append(n)
                n = 0
            byte = f.read(1)
        # appending last chunk
        buffer.append(n)
        '''

        if len(buffer) == 1:
            return (False, buffer[0])
        '''
        else:
            if buffer[1] == 0:
                return (False, buffer[0])
            elif 0 in buffer:
                return (True, buffer[:buffer.index(0)])
        '''
        f.close()
        return (True, self.header, buffer)

    def inverseF(self, num, base):
        '''
            reverse function of F
        '''
        '''
        value = []
        res = num #int(num)
        b = base#int(base)

        while res != 0:
            # prendo il resto tra res e base
            resto = res%b
            #print("resto: ", resto)
            value.append(chr(resto))
            res = (res - resto)/b

        # returning the old content
        return "".join(value[::-1])
        '''
        print(num)
        byte = num.to_bytes(base, "big")
        return byte

    def encode(self, pubkey):
        '''
            RSA encoding

            - leggo il file
            - creo un buffer convertendo tutto il fottuto file in numeri
        '''

        # getting values with pubkey
        e, n = pubkey

        # opening file and creating buffer
        flag, header, number = self.F(self.file, 256, self.n)
        f = open("static/encoded.tga", "wb")
        # writing header first
        #print("header: ", header)
        f.write(self.header)

        if flag:
            # abbiamo una lista di numeri di merda
            self.C = []
            threads = []
            for n in number:
                #temp = long(n**self.e)#long(float(n)) ** long(float(self.e))
                #message = long(temp%self.n)#temp%long(float(self.n))
                message = pow(n, self.e, self.n)
                #print(self.inverseF(message, 257))
                f.write(self.inverseF(message, self.chunks+1))
                #print("..\r")
                self.C.append(message)

        else:
            temp = long(number**self.e)#long(float(number)) ** long(float(self.e))
            message = long(temp%self.n)#temp%long(float(self.n))
            self.C = message

        f.close()


    def decode(self, message):

        outfile = open("static/decoded.tga", "wb")
        # writing header
        outfile.write(self.header)

        print("inside decode")
        n, d = self.privkey
        buffer = []
        if isinstance(message, list):
            # parsing every part of message
            for m in message:
                #temp = long(m**d)#long(float(m)) ** long(float(d))#pow(long(self.message), d)
                #M = long(temp%n)#int(temp%long(float(n)))
                M = pow(m, self.d, self.n)
                #print("temp: ", temp)
                #print("d: ", d)
                #print("M: ", M)
                #print("m: ", m)
                #print("n: ", n)
                buffer.append(M)
                # print(to file)
                #print(self.inverseF(M, 257).decode("hex"))
                #print("__\r")
                #outfile.write(self.inverseF(M, 257))
        else:
            temp = long(message**d)#long(float(message)) ** d#pow(long(self.message), d)
            M = long(temp%n)
            # print(to file)
            buffer.append(M)
            #outfile.write(self.inverseF(M, 257))
        print("stampo su file..")
        for b in buffer:
            outfile.write(self.inverseF(b, self.chunks))
        outfile.close()

    def init_calc(self, p, q):
        # creating mod and product
        print("P: ", p, "Q: ", q)
        self.chunks = 0
        self.n = p * q
        self.phi = (p-1) * (q-1)
        print("N:", self.n, " PHI: ", self.phi)

        for i in range(0,10):
            if pow(256,i)>self.n:
                self.chunks = i-1
                break
        print("Chunks: ", self.chunks)

        # choosing e
        flag, self.e = getCoprime(self.phi)
        print("E: ", self.e)

        if flag:
            # choosing d
            self.d = self.getD()
            print("D: ", self.d)
            print("---------------------------------------------")
            # salviamo chiave pubblica e privata
            self.pubkey = (self.n, self.e)
            self.privkey = (self.n, self.d)


    def bruteforce(self, message, numbit, md5):

        # storing info for keys
        self.numbit = int(numbit)
        self.primeLength = int(self.numbit)#/2)
        # creating prime numbers
        try:
            from pyprimes import primes, prime_count

            # creating reference min value and max value
            minValue = int("1".ljust(self.primeLength, "0"))
            maxValue = int("9".ljust(self.primeLength, "9"))

            numprimes = prime_count(maxValue) - prime_count(minValue)
            iterator = primes(minValue, maxValue)
            primesList = [next(iterator) for num in range(0, numprimes)]
            print("inizio combinations")
            combinationlist = list(itertools.combinations(primesList, 2))
            print("fine combinations")
            for cl in combinationlist:
                p, q = cl
                self.init_calc(p, q)
                if (self.n < 256):
                    continue
                outfile = open("static/bruteforce.tga", "wb")
                # writing header
                outfile.write(self.header)

                print("inside decode")
                n, d = self.privkey
                buffer = []
                if isinstance(message, list):
                    # parsing every part of message
                    for m in message:
                        #temp = long(m**d)#long(float(m)) ** long(float(d))#pow(long(self.message), d)
                        #M = long(temp%n)#int(temp%long(float(n)))
                        M = pow(m, self.d, self.n)
                        #print("temp: ", temp)
                        #print("d: ", d)
                        #print("M: ", M)
                        #print("m: ", m)
                        #print("n: ", n)
                        buffer.append(M)
                        # print(to file)
                        #print(self.inverseF(M, 257).decode("hex"))
                        #print("__\r")
                        #outfile.write(self.inverseF(M, 257))
                else:
                    temp = long(message**d)#long(float(message)) ** d#pow(long(self.message), d)
                    M = long(temp%n)
                    # print(to file)
                    buffer.append(M)
                    #outfile.write(self.inverseF(M, 257))
                print("stampo su file..")
                try:
                    for b in buffer:
                        outfile.write(self.inverseF(b, self.chunks))
                    outfile.close()
                except Exception as e:
                    print(e)
                    outfile.close()
                    continue
                if get_md5_file(outfile) == self.md5:
                    print("TROVATO! chiave: ", self.privkey)
                    break

            self.gotError = False
        except Exception as e:
            print("Yo, missing pyprimes! run 'pip install pyprimes'")
            self.gotError = True
            raise

