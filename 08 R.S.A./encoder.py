class Encoder:

    def __init__(self, file, numbit):
        '''
            RSA encoding

            - scelta di "p" e "q"
        '''
        print "---------- RSA ----------"
        print " p = prime number"
        print " q = prime number"
        print " n = p * q"
        print " prod = (p - 1) * (q - 1)"
        print "-------------------------"
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

            # creating mod and product
            self.n = self.p * self.q
            self.prod = (self.p-1) * (self.q-1)

            self.gotError = False
        except Exception, e:
            print "Yo, missing pyprimes! run 'pip install pyprimes'"
            self.gotError = True
            raise

    def encode(self):
        '''
            RSA encoding

            - cripto il messaggio in base ai dati creati prima
        '''
        if self.gotError:
            return

        f = open(self.file, "rb")
