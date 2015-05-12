import os
import sys
import random

#from decoder import Decoder
#from encoder import Encoder
from client import Client

if __name__ == '__main__':

    # checking arguments
    if len(sys.argv) < 3:
        print("BAD USAGE:")
        print("python rsa.py encode filename len")
        print("python rsa.py decode filename ???")
        print("python rsa.py bruteforce filename md5")
        sys.exit(0)

    print("RSA")

    # selected mode
    mode = sys.argv[1]

    # selected filename
    filename = sys.argv[2]
    len = sys.argv[3]

    # check if file exists
    if not os.path.isfile(filename):
        print("ERROR: File doesn't exist.")
        sys.exit(0)

    # creating encoder or decoder
    if mode == 'encode':
        print('Encoding ...')
        #Encoder(filename, len).encode()
        e = Client(filename, len)
        e.encode(e.pubkey)
        e.decode(e.C)
    elif mode == 'decode':
        key = sys.argv[3]
        print('Decoding ...')
        Decoder(filename, len).decode()
    elif mode == 'bruteforce':
        #selected key
        key_len = sys.argv[3]
        e = Client(filename, len)
        e.encode(e.pubkey)
        e.bruteforce(e.C, key_len, e.md5)
