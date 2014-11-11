import importlib
import importlib.abc

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
        self.value = next(input) & 0xFF
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

class BFLoader(importlib.abc.SourceLoader):
    """
    Python module loader for Brainfuck.

    It is implemented this way because `eval` doesn't work on blocks and
    the effect of `exec` is optimized out when not using the interactive
    Python interpreter.
    """

    def get_data(self, path):
        """
        Overrides ResourceLoader.get_data.
        
        Path is abused to pass the brainfuck code that will be compiled into
        Python.
        """

        brainfuck = self.__preprocess(path)
        self.__validate(brainfuck)
        python = self.__compile(brainfuck)
        return python

    def get_filename(self, fullname): return fullname

    def module_repr(self): return repr(self)

    def __preprocess(self, code):
        chars = frozenset('+-><,.[]')
        return ''.join(filter(lambda x: x in chars, code))

    def __validate(self, code):
        d = 0

        for opcode in code:
            if   opcode == '[': d += 1
            elif opcode == ']': d -= 1

            if d < 0: raise ImportError('Mismatched ]')

        if d != 0: raise ImportError('Mismatched [')

    def __compile(self, brainfuck):
        python  = 'def eval(datasize, input, steps):\n'
        python += '\tc=0;i=input;o=[];p=0;S=datasize;T=steps;m=[0]*S\n'
        python += '\twhile True:\n'
        d = 2

        for opcode in brainfuck:
            python += '\t' * d
            python += 'c+=1\n'
            python += '\t' * d
            python += 'if T<c: return o\n'
            python += '\t' * d

            if   opcode == '+': python += 'm[p]=m[p]+1&255'
            elif opcode == '-': python += 'm[p]=m[p]-1&255'
            elif opcode == '>': python += 'p=(p+1)%S'
            elif opcode == '<': python += 'p=(p-1)%S'
            elif opcode == ',': python += 'm[p]=next(i)&255'
            elif opcode == '.': python += 'o.append(m[p])'
            elif opcode == '[':
                python += 'while m[p]>0:'
                d += 1
            else: d -= 1

            python += '\n'

        return python

class BFJIT(object):
    """Brainfuck to Python JIT compiler."""

    __loader = BFLoader()

    def __init__(self, code, datasize):
        self.__module = BFJIT.__loader.load_module(code)
        self.__datasize = datasize

    def eval(self, input, steps):
        return self.__module.eval(self.__datasize, input, steps)
