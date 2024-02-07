# %%

from pwn import *

# ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=dd1b55c9ef54eabfd21ced9c27cec4dd2b050504, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

# %%

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h"]

argv = ['./src/re3.bin']

gdbscript = 'gef\ngef\n'
gdbscript += 'set follow-fork-mode child\n'

# conn = gdb.debug(argv, gdbscript)

conn = remote('34.123.210.162', 20231)
# conn = process(argv)

# _pid = gdb.attach(conn, gdbscript)

# %%

print("1")
conn.recvuntil(b"Done: ")
conn.sendline(b"2")

print("2")
conn.recvuntil(b"username is: ")
_code = conn.recvline().strip()
_code = int.from_bytes(_code, 'little')
print(f"{_code = }")

print("3")
conn.recvuntil(b"Done: ")
conn.sendline(b"1")

print("4")
conn.recvuntil(b"Username: ")
conn.sendline(b"admin")

print("5")
conn.recvuntil(b"Done: ")
conn.sendline(b"3")

print("6")
conn.recvuntil(b"code: ")
conn.sendline(str(_code).encode())

print("7")
conn.interactive()

# poctf{uwsp_7h3_1355_y0u_kn0w_7h3_837732}
