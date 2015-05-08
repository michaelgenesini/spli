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
        val = 1
        while (val*self.e)%self.phi != 1:
            val += 1
        return val

    def F(self, file, base):
        '''
        converting file to numbers
        '''

        # opening file
        f = open(file, "rb")
        n = 0

        byte = f.read(1)
        while byte:
            n = (n*base) + ord(byte)
            byte = f.read(1)

        return n

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
        number = self.F(self.file, 300)
        #content = self.inverseF(number, 300)   

        self.message = pow(number, self.e)%self.n

        print "number: ", number
        print "message: ", self.message
        print "crypted: ", self.inverseF(self.message, 300)

    def decode(self):

        temp = long(float(self.message)) ** self.d#pow(long(self.message), self.d)
        self.decoded = temp%int(self.n)

        print self.decoded
        print self.inverseF(self.decoded, 300)



