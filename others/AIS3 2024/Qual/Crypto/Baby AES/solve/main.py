# %%

from pwn import *

from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from base64 import b64encode, b64decode

# %%

# nc chal1.eof.ais3.org 10003
r = remote('10.105.0.21', 10003)

r.recvuntil(b"c1_CFB: ")
res = r.recvline().strip()
print(res)

iv_0, c1_ct = eval(res)
iv_0 = b64decode(iv_0)
c1_ct = b64decode(c1_ct)

r.recvuntil(b"c2_OFB: ")
res = r.recvline().strip()
print(res)

iv_1, c2_ct = eval(res)
iv_1 = b64decode(iv_1)
c2_ct = b64decode(c2_ct)

r.recvuntil(b"c3_CTR: ")
res = r.recvline().strip()
print(res)

iv_2, c3_ct = eval(res)
iv_2 = b64decode(iv_2)
c3_ct = b64decode(c3_ct)

print(f"{iv_0 = }")
print(f"{c1_ct = }")
print(f"{iv_1 = }")
print(f"{c2_ct = }")
print(f"{iv_2 = }")
print(f"{c3_ct = }")
print()

# %%

r.interactive()

# %%

# from os import urandom

# counter = urandom(16)

# c1 = urandom(32)
# c2 = urandom(32)

# print(len(counter))  # 16
# print(len(c1))  # 32
# print(len(c2))  # 32
