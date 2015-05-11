from utils import *
from bitarray import bitarray

class Client:

    def __init__(self, file, numbit):
        '''
            RSA encoding

            - scelta di "p" e "q"
        '''
        print "-------------------- RSA --------------------"
        print " p = prime number"
        print " q = prime number"
        print " n = p * q"
        print " phi = (p - 1) * (q - 1)"
        print " e -> 1 < e < phi(n), GCD(e, phi) = 1"
        print " d -> "
        print "---------------------------------------------"
        # storing file
        self.file = file
        # storing info for keys
        self.numbit = int(numbit)
        self.primeLength = int(self.numbit)#/2)
        # creating prime numbers
        try:
            from pyprimes import primes_above, prime_count

            # creating reference min value and max value
            minValue = int("1".ljust(self.primeLength, "0"))
            maxValue = int("9".ljust(self.primeLength, "9"))

            numprimes = prime_count(maxValue) - prime_count(minValue)
            iterator = primes_above(minValue)
            primesList = [next(iterator) for num in range(0, numprimes)]

            # creatint p and q
            ref = int(round(len(primesList)/3))
            self.p = primesList[ref]
            self.q = primesList[-ref]
            print "P: ", self.p, " Q:", self.q

            # creating mod and product
            self.n = self.p * self.q
            self.phi = (self.p-1) * (self.q-1)
            print "N:", self.n, " PHI: ", self.phi

            # choosing e
            flag, self.e = getCoprime(self.phi)
            print "E: ", self.e

            if flag:
                # choosing d
                self.d = self.getD()
                print "D: ", self.d

                # salviamo chiave pubblica e privata
                self.pubkey = (self.n, self.e)
                self.privkey = (self.n, self.d)

            self.gotError = False
        except Exception, e:
            print "Yo, missing pyprimes! run 'pip install pyprimes'"
            self.gotError = True
            raise

    def getD(self):
        '''
        val = 1
        while (val*self.e)%self.phi != 1:
            val += 1
        print "about to return D"
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
        #header = f.read(18)
        # now only body
        n = long(0)
        buffer = []
        byte = f.read(1)
        while byte:
            n = long((n*base) + ord(byte))
            #if n > size:
            if ((n*base) + 255) > size:
                buffer.append(n)
                n = 0
            byte = f.read(1)
        # appending last chunk
        buffer.append(n)

        if len(buffer) == 1:
            return (False, buffer[0])
        '''
        else:
            if buffer[1] == 0:
                return (False, buffer[0])
            elif 0 in buffer:
                return (True, buffer[:buffer.index(0)])
        '''
        return (True, buffer)

    def inverseF(self, num, base):
        '''
            reverse function of F
        '''

        value = []
        res = num #int(num)
        b = base#int(base)

        while res != 0:
            # prendo il resto tra res e base
            resto = int(res%b)
            #print "resto: ", resto
            value.append(bin(resto)[2:])
            res = (res - resto)/b

        # returning the old content
        return bitarray("".join(value[::-1]))

    def encode(self, pubkey):
        '''
            RSA encoding

            - leggo il file
            - creo un buffer convertendo tutto il fottuto file in numeri
        '''
        # getting values with pubkey
        e, n = pubkey

        # opening file and creating buffer
        flag, number = self.F(self.file, 257, self.n)
        #f = open("encoded.jpg", "wb")
        # writing header first
        #f.write(self.header)

        if flag:
            # abbiamo una lista di numeri di merda
            self.C = []
            threads = []
            for n in number:
                temp = long(n**self.e)#long(float(n)) ** long(float(self.e))
                message = long(temp%self.n)#temp%long(float(self.n))
                #print self.inverseF(message, 257)
                #f.write(self.inverseF(message, 257))
                #print "..\r"
                self.C.append(message)
        else:
            temp = long(number**self.e)#long(float(number)) ** long(float(self.e))
            message = long(temp%self.n)#temp%long(float(self.n))
            self.C = message

        #f.close()


    def decode(self, message):

        outfile = open("decoded.txt", "wb")
        # writing header
        #outfile.write(self.header)

        print "inside decode"
        n, d = self.privkey
        buffer = []
        if isinstance(message, list):
            # parsing every part of message
            for m in message:
                temp = long(m**d)#long(float(m)) ** long(float(d))#pow(long(self.message), d)
                M = long(temp%n)#int(temp%long(float(n)))
                print "temp: ", temp
                print "d: ", d
                print "M: ", M
                print "m: ", m
                print "n: ", n
                sys.exit(1)
                buffer.append(M)
                # print to file
                #print self.inverseF(M, 257).decode("hex")
                #print "__\r"
                #outfile.write(self.inverseF(M, 257))
        else:
            temp = long(message**d)#long(float(message)) ** d#pow(long(self.message), d)
            M = long(temp%n)
            # print to file
            buffer.append(M)
            #outfile.write(self.inverseF(M, 257))
        print "stampo su file.."
        for b in buffer:
            outfile.write(self.inverseF(b, 257))
        outfile.close()



