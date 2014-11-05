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
        self.__code  = code
        self.__data  = [ 0 ] * datasize
        self.__pc    = 0
        self.__ptr   = 0
        self.__stack = []

    @property
    def value(self):
        return self.__data[self.__ptr]

    @value.setter
    def value(self, value):
        self.__data[self.__ptr] = value

    @property
    def opcode(self):
        return self.__code[self.__pc]

    def __next(self):
        self.__pc = (self.__pc + 1) % len(self.__code)

    def __plus(self):
        self.value = (self.value + 1) & 0xFF
        self.__next()

    def __minus(self):
        self.value = (self.value - 1) & 0xFF
        self.__next()

    def __right(self):
        self.__ptr = (self.__ptr + 1) % len(self.__data)
        self.__next()

    def __left(self):
        self.__ptr = (self.__ptr - 1) % len(self.__data)
        self.__next()

    def __read(self, input):
        self.value = next(input)
        self.__next()

    def __write(self, output):
        output.append(self.value)
        self.__next()

    def __open(self):
        self.__next()
        if self.value == 0:
            depth = 1
            while depth > 0:
                if self.opcode == '[':
                    depth += 1
                elif self.opcode == ']':
                    depth -= 1
                self.__next()
        else:
            self.__stack.append(self.__pc)

    def __close(self):
        if self.value == 0:
            self.__stack.pop()
            self.__next()
        else:
            self.__pc = self.__stack[-1]

    def eval(self, input, steps):
        output = []
        for i in range(steps):
            if   self.opcode == '+': self.__plus()
            elif self.opcode == '-': self.__minus()
            elif self.opcode == '>': self.__right()
            elif self.opcode == '<': self.__left()
            elif self.opcode == '.': self.__write(output)
            elif self.opcode == ',': self.__read(input)
            elif self.opcode == '[': self.__open()
            elif self.opcode == ']': self.__close()
            else: self.__next()
        return output
