#def bin (s):
#    return str(s) if s<=1 else bin(s>>1) + str(s&1)

import itertools
import operator

MAX = 122
MIN = 97

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

def findKey(crypted, origin):
    if (crypted - origin) >= 0:
        return crypted - origin
    return MAX - MIN + crypted - origin

def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        # print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index
    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]
