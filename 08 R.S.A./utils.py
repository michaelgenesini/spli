def fileToNum(file, base):
    '''
    converting file to numbers
    '''

    # opening file
    f = open(file, "rb")
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

def NumToText(num, base):
    '''
        reverse function of fileToNum
    '''

    value = []
    res = int(num)
    b = int(base)

    print "res", res
    print "b", b
    while res != 0:
        # prendo il resto tra res e base
        resto = res%b
        print "resto ", resto
        value.append(chr(resto))
        print chr(resto)
        res = (res - resto)/b
        print "next value ", res

    # returning the old content
    return "".join(value)