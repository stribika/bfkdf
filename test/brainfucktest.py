#!/usr/bin/python

import collections
import random
import sys

sys.path.append('../main')

from brainfuck import *
from prng import AESCTR

bfg = BFG(AESCTR(b'\x00' * 32, b'\x00' * 16))

for i in range(0, 1024):
    bf = bfg.random_bf(i)
    print(bf)
    assert isinstance(bf, collections.Iterable), 'result is not iterable'
    assert len(bf) == i, 'incorrect result length'
    d = 0
    for ch in bf:
        if ch == '[':
            d += 1
        elif ch == ']':
            d -= 1
        assert d >= 0, 'mismatched ]'
    assert d == 0, 'mismatched ['


bfvm = BFVM('+[>,.<]', 2)

input = iter(range(1000))
output = bfvm.eval(input, 2 + 5 * 1000)
print(output)
assert list(range(1000)) == output, 'cat failed'
