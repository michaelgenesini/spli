from math import *
from fractions import gcd

def fileToNum(file, base):
    '''
    converting file to numbers
    '''

    # opening file
    f = open(file, "rb")
    '''
    value = ""

    byte = f.read(1)
    while byte:
        value += str(ord(byte))
        byte = f.read(1)

    res = 0
    for i in range(len(value)):
        res += int(value[i]) * (int(base)**(len(value) - i - 1))

    #joined = "".join([str(el) for el in value])
    # returning value
    return res
    '''
    n = 0

    byte = f.read(1)
    while byte:
        n = (n*base) + ord(byte)
        byte = f.read(1)

    return n

def NumToText(num, base):
    '''
        reverse function of fileToNum
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
    
'''
def getGCD(v1, v2):
    # trovo il massimo comune divisore
    while (v1 != 0 and v2 != 0):
        if (v1 > v2):
            v1 %= v2
        else:
            v2 %= v1
    return max(v1, v2)
'''

def getCoprime(phi):
    val = 3
    found = False

    # vado avanti fino a quando val != phi
    while val < phi:
        if gcd(val, phi) == 1:
            found = True
            return (found, val)
        val += 1

    # non ho trovato il coprimo, ritorno None
    return (found, None)




