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
        print("---------------------------------------------")

        self.md5 = get_md5_file(file)
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
            print("P: ", self.p)
            print("Q:", self.q)

            # creating mod and product
            self.chunks = 0
            self.n = self.p * self.q
            self.phi = (self.p-1) * (self.q-1)
            print("PHI: ", self.phi)

            for i in range(0,10):
                if pow(256,i)>self.n:
                    self.chunks = i-1
                    break
            print("Chunks (numbers of bytes): ", self.chunks)

            # choosing e
            flag, self.e = getCoprime(self.phi)
            print("\nPublic Key")
            print("E: ", self.e)
            print("N:", self.n)

            if flag:
                # choosing d
                self.d = self.getD()
                print("Private Key")
                print("D: ", self.d)
                print("N:", self.n)

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
        f = open("static/imgs/encoded.tga", "wb")
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

        outfile = open("static/imgs/decoded.tga", "wb")
        # writing header
        outfile.write(self.header)
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
        for b in buffer:
            outfile.write(self.inverseF(b, self.chunks))
        outfile.close()

    def bruteforce(self, message, md5):

        # storing info for keys
        self.primeLength = 7
        # creating prime numbers
        try:
            from pyprimes import primes, prime_count

            for i in range(1, self.primeLength):
                # creating reference min value and max value
                minValue = int("1".ljust(i, "0"))
                maxValue = int("9".ljust(i, "9"))
                found = False

                numprimes = prime_count(maxValue) - prime_count(minValue)
                iterator = primes(minValue, maxValue)
                primesList = [next(iterator) for num in range(0, numprimes)]
                combinationlist = list(itertools.combinations(primesList, 2))
                for cl in combinationlist:
                    p, q = cl
                    if (( p * q ) == self.n):
                        self.p, self.q = p, q
                        found = True
                        break
                if found:
                    break

            print("")
            print("---------------------------------------------")
            print("BRUTEFORCE")
            print("---------------------------------------------")
            print("P: ", self.p," Q: ", self.q)
            self.phi = (self.p-1)*(self.q-1)
            self.d = self.getD()
            print("N: ", self.n," PHI: ", self.phi)
            print("E: ", self.e,"D: ",self.d)
            for i in range(0,10):
                if pow(256,i)>self.n:
                    self.chunks = i-1
                    break
            print("---------------------------------------------")
            self.privkey = (self.n, self.d)

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

            outfile = open("static/imgs/bruteforce.tga", "wb")
            outfile.write(self.header)
            for b in buffer:
                outfile.write(self.inverseF(b, self.chunks))
            outfile.close()
            #if get_md5_file(outfile.name) == self.md5:
            print("TROVATO! chiave: ", self.privkey)

            self.gotError = False
        except Exception as e:
            print("Yo, missing pyprimes! run 'pip install pyprimes'")
            self.gotError = True
            raise

