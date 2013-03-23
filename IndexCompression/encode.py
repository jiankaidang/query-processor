import sys


##def base62encode(number):
##    if not isinstance(number, (int, long)):
##        raise TypeError('number must be an integer')
##    if number < 0:
##        raise ValueError('number must be positive')
##    
##    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
##    re
##    base62 = ''
##    while number:
##        number, i = divmod(number, 62)
##        base62 = alphabet[i] + base62
##
##    return base62 or alphabet[0]
##
##def base62decode(str):
##    return int(str,62)


def decode7bit(bytes):
    bytes = list(bytes)
    value = 0
    shift = 0
    while True:
        byteval = ord(bytes.pop(0))
        if (byteval & 128) == 0: break
        value |= ((byteval & 0x7F) << shift)
        shift += 7
    return (value | (byteval << shift))


def encode7bit(value):
    temp = value
    bytes = ""
    while temp >= 128:
        bytes += chr(0x000000FF & (temp | 0x80))
        temp >>= 7
    bytes += chr(temp)
    return bytes


def main(argv):
##    print base62encode(1)
##    print base62decode('q2a')
##    print base62encode(200048)
    x = encode7bit(1000)
    print x
    print decode7bit(x)
    str_ = 'a' + x + ' ' + 'u'
    print str_


if __name__ == "__main__":
    main(sys.argv)
