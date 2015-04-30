from utils import *

import traceback

class Encoder:

    def __init__ (self, file, chunk_len, k):
        # storing file and key to encode
        self.file = file
        self.k = k
        self.f = []
        # storing output file destination
        #self.output = file.split(".")[0] + "_encoded." + file.split(".")[1]

    def encode (self):
        print "Encoding..."
        # open the input file
        f = open(self.file, "rb")
        # creating output file
        #out = open(self.output, "wb")
        try:
            byte = f.read(2)
            while byte != "":
                chunk = []
                c = ""
                for b in byte:
                    c = c + charToBin(b)
                chunk.append(c)
                byte = f.read(2)
                if byte != "":
                    c = ""
                    for b in byte:
                        c = c + charToBin(b)
                    chunk.append(c)
                self.f.append(chunk)
                byte = f.read(2)
            print self.f
        except Exception, e:
            traceback.print_exc()
        finally:
            print "[encoding] closing files"
            # alla fine chiudo i files
            f.close()
            #out.close()
        self.func(self.f[0],self.k)
    def func (self,chunk,k):
        print "NOT: ", k[1]
        for c in k[1]:
            print c