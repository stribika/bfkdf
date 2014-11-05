import Crypto.Util.Counter
from Crypto.Cipher import AES
from math import ceil
from math import log

def to_int(b):
    num = 0
    for i in range(len(b)):
        num |= b[i] << (i * 8)
    return num

class AESCTR(object):
    def __init__(self, key, iv):
        self.__aes = AES.new(
            key, 
            AES.MODE_CTR,
            counter = Crypto.Util.Counter.new(
                128,
                initial_value = to_int(iv),
                allow_wraparound = True
            )
        )

    def randint(self, min, max):
        if max < min:
            raise Exception('max < min')
        elif min == max:
            return min
        bit_length = ceil(log(max - min, 2))
        byte_length = ceil(bit_length / 8)
        mask = (1 << bit_length) - 1

        while True:
            rand = self.__aes.encrypt(b'\x00' * byte_length)
            num = to_int(rand) & mask
            if num <= max - min:
                return min + num
    
    def bytes(self):
        while True:
            yield self.__aes.encrypt(b'\x00')[0]
