import brainfuck
import scrypt
import prng

def hash(password, salt):
    k0 = scrypt.hash(password, salt, 512, 4, 8, 96)
    code_key = k0[ 0:32]
    data_key = k0[32:64]
    code_iv  = k0[64:80]
    data_iv  = k0[80:96]
    code_rng = prng.AESCTR(code_key, code_iv)
    data_rng = prng.AESCTR(data_key, data_iv)
    code = brainfuck.BFG(code_rng).random_bf(1024)
    print(code)
    vm = brainfuck.BFVM(code, 65536)
    b = vm.eval(data_rng.bytes(), 1000000)
    print(b)

