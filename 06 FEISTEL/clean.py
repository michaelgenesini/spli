import os
import sys
import random

from utils import *

if __name__ == '__main__':

    print "File Cleaner"

    FILE_START = '0000: 0000 0200'
    FILE_END = 'Transfer complete...'

    # selected mode
    filename = sys.argv[1]
    outname = filename.split(".")[0]+"_cleaned.tga"#+filename.split(".")[1]

    outfile = open(outname, "wb")

    # opening file
    f = open(filename, "rb");

    # continuo a leggere fino all'inizio del file
    line = f.readline()
    while FILE_START not in line:
        line = f.readline()

    '''
        line contiene l'inizio del file scambiato
        inizio a scrivere su out file
    '''

    buffer = []
    while FILE_END not in line:
        #outfile.write(line.split(": ")[1].split("  ")[0])
        #towrite = line[6:85].replace("\t", "")
        temp = line[6:85].split(" ")
        for i in range(0, len(temp)):
            if temp[i] != "":
                buffer.append(temp[i])
        line = f.readline()

    counter = 0;
    for s in buffer:
        print s
        print counter
        outfile.write(s.decode("hex"))
        '''
        counter += 1
        if counter == 8:
            outfile.write("\n")
            counter = 0
        '''

    # closing files
    f.close()
    outfile.close()