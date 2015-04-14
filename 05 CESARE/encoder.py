from utils import charToBin

import traceback

class Encoder:

    def __init__ (self, file, key):
        # storing file and key to encode
        self.file = file
        self.key = key
        # storing output file destination
        self.output = file.split(".")[0] + "_encoded." + file.split(".")[1]

    def encode (self):
        '''
            encode
                read every byte of the input file
                move every byte by key value
                write byte in output file

                input: test.txt
                output: test_encoded.txt
        '''
        # open the input file
        f = open(self.file, "rb")
        f.seek(0)
        # creating output file
        out = open(self.output, "wb")
        out.seek(0)
        try:
            byte = f.read(1)
            while byte != "":
                # ho letto un byte, lo stampo
                # processo il byte appena letto
                toWrite = int(charToBin(byte), 2) + self.key
                #out.write(bytearray(int(str(toWrite), 2)))
                out.write(bytes("\x"+str(toWrite)))
                # ne leggo un altro
                byte = f.read(1)
        except Exception, e:
            traceback.print_exc()
        finally:
            print "[encoding] closing files"
            # alla fine chiudo i files
            f.close()
            out.close()