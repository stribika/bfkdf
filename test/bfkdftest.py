#!/usr/bin/python

import collections
import random
import sys

sys.path.append('../main')

import bfkdf

bfkdf.hash(b'', b'')

bfkdf.hash(b'password', b'NaCl')

bfkdf.hash(b'pleaseletmein', b'SodiumChloride')
