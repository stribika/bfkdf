class BFG(object):
    """The Brainfuck generator"""

    def __init__(self, random_source):
        self.__random_source = random_source

    def random_bf(self, size):
        buffer = [ ' ' ] * size
        self.__random_bf_r(buffer, 0, size)
        return ''.join(buffer)

    def __random_bf_r(self, buffer, offset, size):
        bf_chars = ( '+', '-', '>', '<', ',', '.', '[', ']' )

        if size < 0:
            raise Exception('size cannot be negative')
        elif size == 0:
            pass
        elif size == 1:
            buffer[offset] = bf_chars[self.__random_source.randint(0, 5)]
        else:
            buffer[offset] = bf_chars[self.__random_source.randint(0, 6)]
            if buffer[offset] == '[':
                k = self.__random_source.randint(1, size - 1)
                self.__random_bf_r(buffer, offset + 1, k - 1)
                buffer[offset + k] = ']'
                self.__random_bf_r(buffer, offset + k + 1, size - k - 1)
            else:
                self.__random_bf_r(buffer, offset + 1, size - 1)

class BFVM(object):
    """The Brainfuck virtual machine"""

    def __init__(self, code, datasize):
        self.__code = code
        self.__data = [ 0 ] * datasize
