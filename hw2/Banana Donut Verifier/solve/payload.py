from pwn import *

filename = '../src/donut-verifier'

_proc: process
_proc = process(filename)

# gdb.attach(_proc, ...
# gdb.debug(filename, ...

# printf 1
# __isoc99_scanf
# printf 1 + 500 (0~499)

# _proc = gdb.debug(
#     filename,

# init gef
gdbscript = 'gef\ngef\n'
# set fork mode
gdbscript += 'set follow-fork-mode child\n'

# info functions

# set breakpoints
gdbscript += 'b printf\nb __isoc99_scanf\nb usleep\n'
# cont. to first breakpoint
gdbscript += 'c\n'

## input here (done by line `sendlineafter`)

# move to right after scanf / right before next instruction
gdbscript += 'n\nn\nn\nn\n'

# $rax   : 0x4
# $rbx   : 0x0
# $rcx   : 0x4a325b1b
# $rdx   : 0x0
# $rsp   : 0x00007ffd1d0d3930  →  0x0000000000000000
# $rbp   : 0x00007ffd1d0d6010  →  0x0000000000000001
# $rsi   : 0x4a325b1b
# $rdi   : 0x00007ffd1d0d33d0  →  0x00007efcb1062050  →  <funlockfile+0> endbr64
# $rip   : 0x000055f0e3530241  →   mov QWORD PTR [rbp-0x28], 0x0
# $r8    : 0x0
# $r9    : 0x000055f0e4c4c6b0  →  "11111111111111111111111111111111111111111111111111[...]"
# $r10   : 0x000055f0e353142f  →   sbb ebx, DWORD PTR [rbx+0x32]
# $r11   : 0x0
# $r12   : 0x00007ffd1d0d6128  →  0x00007ffd1d0d7c64  →  "../src/donut-verifier"
# $r13   : 0x000055f0e35301a9  →   push rbp
# $r14   : 0x000055f0e3534dc8  →  0x000055f0e3530160  →   endbr64
# $r15   : 0x00007efcb14c0040  →  0x00007efcb14c12e0  →  0x000055f0e352f000  →   jg 0x55f0e352f047
# $eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
# $cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00

# gdbscript += 'clear printf\nclear __isoc99_scanf\n'
# gdbscript += 'c\n'

# walk out from the main loop (the stack will got same layout as right before walk into the main loop)
# gdbscript += 'n\nn\nn\n'

###

_pid = gdb.attach(
    _proc,
    gdbscript=gdbscript,
)

a = _proc.sendlineafter(b'Dount Verifier\n', b"1" * 1024)
print(a)

a = _proc.recvall()
print(a)

print("HI")

###

# input store at
# [rsp+2260h] [rbp-480h]
# 0x2260 = 8800

# cmp arr is off_6050[0] (aka. byte_2010) at 0x2010 + 1024 = 0x2410

###

# 0xc0f0 (the addr right before THE arr on the stack) 0x9e90 ($sp) => 8800
# 8800 / 16 = 550
# 550 * 4 = 2200

### context

# 0x7fff2666e5a8: 0x00000000      0x00000000      0x00000000      0x00000000
# 0x7fff2666e5b8: 0x003055e4      0x00000000      0x33323130

# $rsp   : 0x00007fff2666c358  →  0x00005595a6e74241  →   mov QWORD PTR [rbp-0x28], 0x0

###

## below three x... cmds have same result shown as next below
# > gef➤  x/2210x $sp
# > gef➤  x/10x ($rsp+0x2260)
# > gef➤  x/10x ($rbp-0x480)
# 0x7ffd76793290: 0x33323130      0x37363534      0x38393938      0x34353637
# 0x7ffd767932a0: 0x30313233      0x00000000      0x00000000      0x00000000
# 0x7ffd767932b0: 0x00000000      0x00000000

###

# 1024 / 4 = 256
# 2200 + 256
# x/2210x $sp -> x/2456x $sp
