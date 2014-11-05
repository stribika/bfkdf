# What?

BFKDF is a key derivation function. It takes a relatively low entropy secret
password and a high entropy but known salt and turns it into a key that can be
used in ciphers and MACs. It does this as expensively as possible to slow down
cracking. This property makes it suitable for various proof-of-work schemes.

# How?

```
 password, salt
     |
     +----------------------------.
     |                            |
     V                            |
 ,--------.                       |
 | scrypt |                       |
 `--------'                       |
     |    pseudorandom input      |
     +----------------------.     |
     | pseudorandom code    |     |
     V                      V     |
   ,--------------------------.   |
   |         brainfuck        |   |
   `--------------------------'   |
                 |                |
                 |                |
                 V                V
            ,--------.       ,--------.
            | scrypt |------>| scrypt |---> key
            `--------'       `--------'
```

Halting problem? Only 1000000 steps are evaluated. The instruction pointer wraps
around when the end of the code is reached, in clear violation of the Brainfuck
standard, ensuring it can always run long enough.

# Why?

Why not use a simple hash function? Hash functions are designed to be quick.
Password checking runs only a few times in the real applications but crackers
have to run it often, therefore it makes sense to slow it down. First PBKDF2 was
created which iterates a hash function to make it slow. However, crackers are
not using the same hardware as users but a parallel and pipelined ASIC/FPGA/GPU
implementation. To counter this, scrypt was created which requires not just a
lot of iterations but lots of memory as well. Crackers in response had to add
memory to their cracking rigs.

BFKDF generates pseudorandom code in a Turing complete language (Brainfuck)
based on the password. The output of this generated program participates in the
final hash. My hope is that ASIC implementations of this algorithm must include
a CPU as well.

Why is there an scrypt before the Brainfuck? Randomly generated code does not
run in constant time. Generating it directly from the password or passing the
password as input would be vulnerable to timing attacks.

Why is there an scrypt after the Brainfuck? To avoid the risk of confusing the
end of the output with the beginning of the password in the final scrypt. Also,
the output is not very random.

Why Brainfuck? It's very easy to generate. Normal languages have strict syntax
rules while Brainfuck's requirements are rather lax. It was also easy to
implement. There are reasons to use something else. Due to "[" and "]" only
distinguishing between zero and non-zero, the output contains too many 0s, 1s,
and 255s. Short infinite loops are also very likely, resulting in short
repeating sequences. Malbolge seems like a better choice but AFAIK it's not
proven to be Turing complete.
