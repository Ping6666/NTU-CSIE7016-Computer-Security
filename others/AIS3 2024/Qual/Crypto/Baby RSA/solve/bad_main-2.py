# %%

from pwn import *

# %%

# nc chal1.eof.ais3.org 10002
r = remote('10.105.0.21', 10002)

print(f"1")
res = r.recvline().strip().decode()

res = res.split(',')
n = int(res[0].split("=")[1])
e = int(res[1].split("=")[1])

print(f"2")
r.recvuntil(b"FLAG:  ")
res = r.recvline().strip().decode()
flag_ct = int(res)

print(f"{n = }")
print(f"{e = }")
print(f"{flag_ct = }")
print()

# %%

xor_len = 8

shift = (1 << xor_len * 8)
left_shift = pow(shift, e, n)
right_shift = pow(shift, -1 * e, n)

# flag_ct_shift = flag_ct << (xor_len * 8)

flag_ct_shift = flag_ct * left_shift

flags = []

print(f"3")
for _ in range(3):

    r.sendlineafter(b"Any message for me?", str(flag_ct_shift).encode())
    r.recvline()

    r.recvuntil(b"New Message:  ")
    res = r.recvline().strip().decode()
    flag_ct = int(res)

    flags.append((flag_ct - flag_ct_shift) % n)
    # flags.append((flag_ct * right_shift) % n)

    print(flag_ct)

# %%

print(flags)
