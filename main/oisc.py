from math import sqrt

class OISCVM(object):
    def __init__(self, data):
        self.__data     = list(data)
        self.__size     = len(data)
        self.__pc       = 0
        self.__level    = int(sqrt(self.__size) / 3)
        self.__maxlevel = int(sqrt(self.__size))
    
    @property
    def data(self): return list(self.__data)

    def eval(self, steps):
        for i in range(steps):
            ( a, b, c ) = (
                self.__lookup(self.__pc),
                self.__lookup(self.__pc + 1),
                self.__lookup(self.__pc + 2),
            )
            self.__the_instruction(a, b, c)
            self.__level = (self.__level + 1) % self.__maxlevel
            
    def __lookup(self, addr):
        result = addr % self.__size
        for i in range(self.__level):
            result = self.__data[result]
        return result
    
    def __the_instruction(self, a, b, c):
        self.__data[a] = (self.__data[a] - self.__data[b]) % self.__size
        if self.__data[a] >= self.__size // 2: # 2's complement negative
            self.__pc = self.__data[c]
