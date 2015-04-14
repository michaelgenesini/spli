#def bin (s):
#    return str(s) if s<=1 else bin(s>>1) + str(s&1)

def charToBin (c):
    s = format(ord(c),'b').zfill(8)
    return "0b" + s