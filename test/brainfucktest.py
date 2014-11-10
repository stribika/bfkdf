#!/usr/bin/python

import collections
import random
import sys

sys.path.append('../main')

from brainfuck import *
from prng import AESCTR

def generator():
    bfg = BFG(AESCTR(b'\x00' * 32, b'\x00' * 16))

    for i in range(0, 1024):
        bf = bfg.random_bf(i)
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
generator()

def cat_normal():
    bfvm = BFVM('+[>,.<]', 2)
    input = iter(range(1000))

    output = bfvm.eval(input, 2 + 5 * 1000)

    assert list(range(1000)) == output, 'cat failed'
cat_normal()

def cat_pc_wrap():
    bfvm = BFVM(',.', 1)
    input = iter(range(1000))

    output = bfvm.eval(input, 2 * 1000)

    assert list(range(1000)) == output, 'cat with PC wrapping failed'
cat_pc_wrap()

def cat_ptr_wrap():
    bfvm = BFVM('+[<,.>]', 2)
    input = iter(range(1000))

    output = bfvm.eval(input, 2 + 5 * 1000)

    assert list(range(1000)) == output, 'cat with PTR wrapping failed'
cat_ptr_wrap()
