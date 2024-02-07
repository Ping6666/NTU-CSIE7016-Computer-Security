from pwn import *

filename = '../src/simple-crackme_0f8aff72e456'

_proc: process
_proc = process(filename)

gdbscript = 'gef\ngef\n'
gdbscript += 'set follow-fork-mode child\n'

# info functions

gdbscript += 'b malloc\nb memcmp\n'
gdbscript += 'c\n'  # exec to first malloc
gdbscript += 'c\n'  # exec to second malloc

# --- 123
# gdbscript += 'b __isoc99_scanf\n'

# n * 8 to next instrunction

# get input_arr addr in $rax
# x/50x 0x000055cd7dfc92d0

### choose 1 or 2

## 1
# ni * 11 into the scanf in the loop
# n * 4 out from the scanf
# ni * 5 end curr loop
# ni * 4 from next loop to the scanf

## 2
# c
# --- 123

# --- 456
# gdbscript += 'c\n'  # exec to third malloc
# gdbscript += 'c\n'  # exec to 4-th malloc
# gdbscript += 'c\n'  # exec to 5-th malloc
# gdbscript += 'c\n'  # exec to 6-th malloc

# n * 8 to next instrunction

# get ret_cmp_arr addr in $rax
# x/50x 0x000055cd7dfc94b0
# --- 456

###

_pid = gdb.attach(
    _proc,
    gdbscript=gdbscript,
)

_proc.sendline(b'49')

payload = [
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

print(f"{payload = }")

for i in range(49):
    _proc.sendline(str(payload[i]).encode())

a = _proc.recvall()
print(a)

print("HI")
