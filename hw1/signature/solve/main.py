# %%

from hashlib import sha256

from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key, Private_key, Signature

from Crypto.Util.number import bytes_to_long

from pwn import *

# %%


class SingletonRemote():
    conn: remote

    def __init__(self):
        self.conn = None

        self.init_conn()
        return

    def __del__(self):
        print("\nClose connection!!!")

        self.cc_conn()
        return

    def cc_conn(self):
        try:
            self.conn.close()
            del self.conn

        except Exception as e:
            print("Closes the tube", e)

        self.conn = None
        return

    def init_conn(self):
        self.cc_conn()

        print("\nNew connection!!!")

        self.conn = remote('10.113.184.121', 10033)
        # self.conn = process(['python', './signature_test.py'])
        return

    def get_rsh(self, byte_str: bytes):

        self.conn.sendlineafter(b"3) exit\n", str(1).encode())
        self.conn.sendlineafter(b'What do you want? ', byte_str)
        self.conn.recvuntil(b"sig = ")

        r, s = eval(self.conn.recvline().decode())
        h = bytes_to_long(sha256(byte_str).digest())

        return r, s, h

    def get_flag(self, r_byte_str: bytes, s_byte_str: bytes):

        self.conn.sendlineafter(b"3) exit\n", str(2).encode())
        self.conn.sendlineafter(b'r: ', r_byte_str)
        self.conn.sendlineafter(b's: ', s_byte_str)

        s = self.conn.recvline(keepends=None).decode()

        return s


# %%

sr = SingletonRemote()

# %%

msg_test = "@_@"

# %%
# --- round 1 --- #

r_1, s_1, h_1 = sr.get_rsh(str(msg_test).encode())

print(f"{r_1 = }")
print(f"{s_1 = }")
print(f"{h_1 = }")
print()

# %%
# --- round 2 --- #

r_2, s_2, h_2 = sr.get_rsh(str(msg_test).encode())

print(f"{r_2 = }")
print(f"{s_2 = }")
print(f"{h_2 = }")
print()

# %%
# --- round 3 --- #

E = SECP256k1
G, n = E.generator, E.order

## --- random ephemeral key --- ##
# s = kE -1 (H + d × r) mod q
# k1 = s1 -1 H1 +  d(s1 -1 r1) mod q
# k2 = s2 -1 H2 + d(s2 -1 r2) mod q
# d = (s1 -1 H1 - s2 -1 H2) / (s2 -1 * r2 - s1 -1 r1)

coef = 1337

# k2 = k1 * coef
# coef * h1 * pow(s1, -1, n) +  coef * d * r1 * pow(s1, -1, n) = h2 * pow(s2, -1, n) + d * r2 * pow(s2, -1, n)
# d = (coef * h1 * pow(s1, -1, n) - h2 * pow(s2, -1, n)) / (r2 * pow(s2, -1, n)  - coef * r1 * pow(s1, -1, n))

d = (coef * h_1 * pow(s_1, -1, n) - h_2 * pow(s_2, -1, n)) * \
    pow((r_2 * pow(s_2, -1, n) - coef * r_1 * pow(s_1, -1, n)), -1, n)

pubkey = Public_key(G, d * G)
prikey = Private_key(pubkey, d)

# %%
msg = 'Give me the FLAG.'

h = sha256(str(msg).encode()).digest()

# %%

# random ephemeral key
k = randint(1, n)

sig = prikey.sign(bytes_to_long(h), k)
flag = sr.get_flag(str(sig.r).encode(), str(sig.s).encode())

# %%

print(f"{flag = }")

# flag = "b'FLAG{EphemeralKeyShouldBeRandom}'"

#%%
