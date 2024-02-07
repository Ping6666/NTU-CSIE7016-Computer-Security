# %%
from pwn import *

from math import log, ceil

from Crypto.Util.number import long_to_bytes

# %%
r = remote('edu-ctf.zoolab.org', 10005)

n = int(r.recvline().decode())
e = int(r.recvline().decode())
enc = int(r.recvline().decode())

# %%
print(n)
print(e)
print(enc)

# %%
mod = 3
mod_inv = pow(mod, -1, n)

lsb = 0
_flag = 0

# %%
for i in range(ceil(log(n) / log(mod))):

    print(long_to_bytes(_flag))
    enc_i = (enc * pow(mod_inv, e * i, n)) % n

    r.sendline(str(enc_i).encode())
    _lsb = int(r.recvline().decode())

    _lsb_i = (_lsb - (lsb * mod_inv) % n) % mod
    lsb = (lsb * mod_inv + _lsb_i) % n

    _flag += _lsb_i * pow(mod, i)

# %%
print(_flag)
print(long_to_bytes(_flag))

# %%
r.close()

# b"FLAG{Viycx_qsklsjgmeld_fgd_spkgjo}\x95\x0b5\x12\xec'fK\x9e\x9f\xd5\xb2\x01\xc7e\x1e\xbe\x86\xcfI\xaa\xc4O\xeb\xd8\xfa\xea\x93\xef\xb2\x9b\xafxUX\xa6\x96$\x8byO\xf4\x03\x05g\x91\xc8\x96N\xaa\x9ao(I\x91\x97\xe5\xb8m&m`O\xcb\xe0\xf7\x1b\x01+\xe6\xde2\x1eBpd\x07?\xf8J\x14\xa51~\x027\xab\x0e\x8d\xbf\x98\x00/\x90\xc3\xc8q\xcdt\x8c\xa5^\x960\x17\xfd\xbb\xf2\x17\x08\xad\xf2y\xcc\x0b\xa0\x02=l\xe4\x9b\x9f\x964\xf79\x96\x9du\xf7\xa8\xed\x1b\xb3\x15\xa4\xdeWr\xcd\xb1;\n\xd9\xc4\x03\x97\x16\x0bK\xbf\x9aG6\xf4`\x0cX@\xd75\x90c\x939_\xb6e\x80\xad\x93l\xa4+\x84\xb8\xf2\xd6\n\x05\x0ba\x83)\x12@8\xaa\xa6@A\n\xb26\xb2\x93\xb1\xa5\xebA\xd7\xbd\xe1}\x84\xd7\x13tj\xd6h\xa7\x9d\x1a\x8d\x88\x1c<\x84[X\x8c"