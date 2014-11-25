import brainfuck
import scrypt
import prng

def hash(password, salt):
    """The hash function you want to call."""

    k0 = scrypt.hash(password, salt, 512, 4, 8, 48)
    debug("k0", k0)
    rng = prng.AESCTR(k0[:32], k0[32:])
    b = run_brainfuck(rng)
    k1 = scrypt.hash(b, salt, 512, 4, 8, 32)
    debug("k1", k1)
    key = scrypt.hash(k1 + password, salt, 512, 4, 8, 32)
    debug("key", key)
    return key

def run_brainfuck(rng):
    """Futile attempt to preseve randomness."""

    output = b''
    
    while len(output) < 48 or len(set(output)) < 44:
        code = brainfuck.BFG(rng).random_bf(1024)
        vm = brainfuck.BFJIT(code, 65536)
        chunk = bytes(vm.eval(rng.bytes(), 1000000))
        debug("chunk", chunk)
        output += chunk

    return output

def debug(label, data):
#    return
    d =  ''.join([ hex(b)[2:].rjust(2, '0') for b in data ])
    d = d if len(d) < 100 else d[:50] + '...' + d[-50:]
    print(label, '=', d, 'bytes =', len(data), 'unique bytes =', len(set(data)))
