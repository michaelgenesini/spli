#def bin (s):
#    return str(s) if s<=1 else bin(s>>1) + str(s&1)

MAX = 256
MIN = 0

def charToBin (c):
    s = format(ord(c),'b').zfill(8)
    return "0b" + s

def inc(value, inc, max):
    if ( value + inc ) < max:
        return value + inc
    return value + inc - max

def dec(value, dec, min):
    if ( value - dec ) >= min:
        return value - dec
    return MAX + (value - dec)
