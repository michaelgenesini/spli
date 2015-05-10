from utils import *

class Encoder:

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
        self.primeLength = int(self.numbit/2)
        # creating prime numbers
        try:
            from pyprimes import primes_above

            # creating reference min value and max value
            minValue = int("1".ljust(self.primeLength, "0"))
            maxValue = int("9".ljust(self.primeLength, "9"))

            iterator = primes_above(minValue)
            primesList = [next(iterator) for num in range(minValue, maxValue)]

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
        n = 0
        buffer = []
        byte = f.read(1)
        while byte:
            n = (n*base) + ord(byte)
            if n > size:
                buffer.append(n)
                n = 0
            byte = f.read(1)
        # appending last chunk
        buffer.append(n)

        if len(buffer) == 1:
            return (False, buffer[0])

        return (True, buffer)

    def inverseF(self, num, base):
        '''
            reverse function of F
        '''

        value = []
        res = int(num)
        b = int(base)

        while res != 0:
            # prendo il resto tra res e base
            resto = res%b
            value.append(chr(resto))
            res = (res - resto)/b

        # returning the old content
        return "".join(value[::-1])

    def encode(self):
        '''
            RSA encoding

            - leggo il file
            - creo un buffer convertendo tutto il fottuto file in numeri
        '''
        if self.gotError:
            return

        # opening file and creating buffer
        flag, number = self.F(self.file, 300, self.n)

        if flag:
            # abbiamo una lista di numeri di merda
            self.C = []
            for n in number:
                temp = long(float(n)) ** long(float(self.e))
                message = temp%long(float(self.n))
                self.C.append(message)

                print "message has been splitted"
                print "number: ", n
                print "message: ", message
                print "crypted: ", self.inverseF(message, 300)
        else:
            temp = long(float(number)) ** long(float(self.e))
            message = temp%long(float(self.n))
            self.C = message
            #content = self.inverseF(number, 300)   

            print "message not splitted"
            print "number: ", number
            print "message: ", self.C
            print "crypted: ", self.inverseF(self.C, 300)

        # INVIO DEL MESSAGGIO DI MERDA.


    def decode(self, message):

        print "inside decode"
        n, d = self.privkey
        if isinstance(message, list):
            # parsing every part of message
            for m in message:
                temp = long(float(m)) ** long(float(d))#pow(long(self.message), d)
                M = int(temp%long(float(n)))

                print M
                print self.inverseF(M, 300)
        else:
            temp = long(float(message)) ** d#pow(long(self.message), d)
            self.M = temp%int(n)

            print self.M
            print self.inverseF(self.M, 300)



