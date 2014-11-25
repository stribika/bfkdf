#!/usr/bin/python

import collections
import profile
import random
import sys

sys.path.append('../main')

from brainfuck import *
from prng import AESCTR

def run_test(test):
    print('Running', test)
    profile.run(test, sort = 2)
    print('Finished', test)

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
run_test('generator()')

def cat_normal(bf_impl):
    bfvm = bf_impl('+[>,.<]', 2)
    input = iter(range(200))

    output = bfvm.eval(input, 2 + 5 * 200)

    assert list(range(200)) == output, 'cat failed'
run_test('cat_normal(BFVM)')
run_test('cat_normal(BFJIT)')

def cat_ptr_wrap(bf_impl):
    bfvm = bf_impl('+[<,.>]', 2)
    input = iter(range(200))

    output = bfvm.eval(input, 2 + 5 * 200)

    assert list(range(200)) == output, 'cat with PTR wrapping failed'
run_test('cat_ptr_wrap(BFVM)')
run_test('cat_ptr_wrap(BFJIT)')

def random_compare():
    bfg    = BFG(AESCTR(b'\xff' * 32, b'\x00' * 16))
    in_int = AESCTR(b'\x00' * 32, b'\xff' * 16)
    in_jit = AESCTR(b'\x00' * 32, b'\xff' * 16)

    for i in range(10):
        bf = bfg.random_bf(1024)
        print(bf)
        bfint = BFVM(bf, 65536)
        bfjit = BFJIT(bf, 65536)
        out_int = bfint.eval(in_int.bytes(), 1000000)
        out_jit = bfjit.eval(in_jit.bytes(), 1000000)
        assert out_int == out_jit, 'interpreted and compiled version different\nout_int={out_int}\nout_jit={out_jit}'.format(out_int=out_int, out_jit=out_jit)
run_test('random_compare()')

