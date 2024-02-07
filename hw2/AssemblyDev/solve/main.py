# %%

from pwn import *

# ref
# https://stackoverflow.com/questions/64482357/x64-asm-moving-a-negative-value-from-a-register-to-memory
# https://stackoverflow.com/questions/40893026/mul-function-in-assembly
# https://stackoverflow.com/questions/48861606/accessing-the-low-32-bits-of-r8-through-r15
# https://stackoverflow.com/questions/40602029/how-to-write-if-else-in-assembly
# https://stackoverflow.com/questions/27284895/how-to-compare-a-signed-value-and-an-unsigned-value-in-x86-assembly
# http://unixwiz.net/techtips/x86-jumps.html
# https://stackoverflow.com/questions/49116747/assembly-check-if-number-is-even
# https://www.felixcloutier.com/x86/mul.html
# https://www.felixcloutier.com/x86/div.html

# %%


def get_asm_b64e(f_name: str):
    return base64.b64encode(open(f_name, 'rb').read())


# %%

r = remote('10.113.184.121', 10020)

r.recvuntil(b"Give me your base64 of your assembly code!\n>")
r.sendline(get_asm_b64e('./solve_q1.asm'))

r.recvuntil(b"Give me your base64 of your assembly code!\n>")
r.sendline(get_asm_b64e('./solve_q2.asm'))

r.recvuntil(b"Give me your base64 of your assembly code!\n>")
r.sendline(get_asm_b64e('./solve_q3.asm'))

r.recvuntil(b"Here is your flag: ")

flag = r.recvline().strip()
print(flag)

r.close()

# FLAG{c0d1Ng_1n_a5s3mB1y_i5_sO_fun!}

# %%
