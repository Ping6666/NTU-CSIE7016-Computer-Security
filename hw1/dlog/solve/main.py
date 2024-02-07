# %%

from Crypto.Util.number import isPrime, getPrime, long_to_bytes

from pwn import *
from sage.all import *

# %%


def get_smooth_prime(bit_len: int = 1024):

    # start from an even number
    n = 2

    # next prime step (in bit)
    bit_step = 10

    while True:
        curr_bit_len = n.bit_length()

        if curr_bit_len > bit_len:
            n = 2

        elif curr_bit_len == bit_len:
            if isPrime(n + 1):
                return n + 1

        n *= getPrime(bit_step)


# %%

p = get_smooth_prime()
g = 7

print(f"{p = }")
print(f"{g = }")

# %%

# r = process(['python', './dlog_test.py'])
r = remote('10.113.184.121', 10032)

r.sendlineafter(b"give me a prime: ", str(p).encode())
r.sendlineafter(b"give me a number: ", str(g).encode())

# %%

r.recvuntil(b'The hint about my secret:')
m = r.recvall().decode().strip()

print(f"{m = }")

# %%

flag = discrete_log(Mod(m, p), Mod(g, p))
flag_byte = long_to_bytes(flag)

print(f"{flag = }")
print(f"{flag_byte = }")

# flag = 165097543714277458627745627326164830149523491597938417175330031130659155467360915745738595625986679363646878333
# flag_byte = b'FLAG{YouAreARealRealRealRealDiscreteLogMaster}'
