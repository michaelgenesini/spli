import os
import sys

from utils import *
from decoder import Decoder
from encoder import Encoder

if __name__ == '__main__':

    # checking arguments
    if len(sys.argv) < 3:
        print "BAD USAGE:"
        print "python feistel.py encode filename key"
        sys.exit(0)
    
    # selected mode
    mode = sys.argv[1]

    # selected filename
    filename = sys.argv[2]

    #selected key
    key = sys.argv[3]

    k = []
    for c in key:
        k.append(charToBin(c)[0:4])
        k.append(charToBin(c)[4:8])

    key_len = len(k)
    times = key_len

    print "K: ",k
    print "Key Len: ",str(key_len)
    print "Times: ", str(times)

    chunk_len = 32

    # printing parameters
    print "Selected mode: " + mode
    print "Selected file: " + filename
    print "Selected key: " + str(k)

    # check if file exists
    if not os.path.isfile(filename):
        print "ERROR: File doesn't exists."
        sys.exit(0)

    # creating encoder or decoder
    if mode == "encode":
        Encoder(filename, chunk_len, k).encode()