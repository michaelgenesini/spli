from utils import *

import imghdr
import traceback

class Decoder:

    def __init__ (self, file, key):
        # storing file and key/mode to decode file
        self.file = file
        self.key = key
        self.extensions = ["rgb", "gif", "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "jpeg", "bmp", "png"]

    def decode (self):
        '''
            decode
                1. apro il file da decodificare
                    ogni byte viene shiftato all'indietro di key
                    scrivo su file.
                2. se non conosciamo la chiave ripetere 1 con 
                    tutte le chiavi possibili da 0 a 255
        '''
        if self.key == "bruteforce":
            # non conosciamo la chiave
            '''
                sovrascrivi sempre lo stesso file di output ad ogni iterazione
                import imghdr
                controlla tipo di immagine con imghdr.what(filename)
                se estensione non in self.extensions allora continua con la prossima
                iterazione, altrimenti abbiamo trovato (probabilmente) la chiave giusta
            '''
            output = self.file.split(".")[0] + "_decoded." + self.file.split(".")[1]
            # open the input file
            f = open(self.file, "rb")
            f.seek(0)
            for _key in range(1,255):
                # creating output file
                out = open(output, "wb")
                out.seek(0)
                try:
                    byte = f.read(1)
                    while byte != "":
                        # ho letto un byte, lo stampo
                        # processo il byte appena letto
                        toWrite = dec(int(charToBin(byte), 2), _key, MIN)
                        out.write(chr(toWrite))
                        # ne leggo un altro
                        byte = f.read(1)
                except Exception, e:
                    traceback.print_exc()
                finally:
                    # alla fine chiudo i files
                    f.seek(0)
                    out.close()
                    pass
                frm = str(imghdr.what(output))
                if frm in self.extensions:
                    print "Key detected: " + str(_key)
                    break
            f.close()
        else:
            output = self.file.split(".")[0] + "_decoded." + self.file.split(".")[1]
            # open the input file
            f = open(self.file, "rb")
            f.seek(0)
            # creating output file
            out = open(output, "wb")
            out.seek(0)
            try:
                byte = f.read(1)
                while byte != "":
                    # ho letto un byte, lo stampo
                    # processo il byte appena letto
                    toWrite = dec(int(charToBin(byte), 2), self.key, MIN)
                    out.write(chr(toWrite))
                    # ne leggo un altro
                    byte = f.read(1)
            except Exception, e:
                traceback.print_exc()
            finally:
                print "[decoding] closing files"
                # alla fine chiudo i files
                f.close()
                out.close()