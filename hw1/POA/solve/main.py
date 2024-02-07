# %%
from pwn import *


# %%
def padding_oracle_attack(r: remote, ct, iv, block_size: int = 16):
    """
    Args:
        ct: current CBC (Cipher-block chaining) ciphertext
        iv: the initialization vector

    """

    _flag = b""

    # solve the block from the back to the front
    for i in reversed(range(block_size)):

        # the plaintext need to be printable characters
        for pt in range(128, 256):

            print(f"\r{bytes([pt ^ 0x80])}  ", end='')
            iv[i] ^= pt

            _line = (bytes(iv + ct).hex().encode())
            r.sendline(_line)
            s = r.recvline()

            if b"Well received :)" in s:
                print()
                _flag = bytes([pt ^ 0x80]) + _flag

                iv[i] ^= 0x80
                break
            else:
                iv[i] ^= pt
        else:
            # meet the pading
            iv[i] ^= 0x80

    return _flag


# %%
r = remote('edu-ctf.zoolab.org', 10004)

# %%
s = r.recvline(keepends=False).decode()
s = bytes.fromhex(s)
print('s', s)

# %%
# 16 bits a block
block_size = 16

iv = s[:16]
ct = s[16:]
flag = b""

# %%
for i in range(len(ct) // block_size):
    block = ct[i * 16:(i + 1) * 16]
    flag += padding_oracle_attack(r, block, bytearray(iv))
    iv = block

print('flag', flag)

# %%
r.close()
