; Challenge Info

; # Modify register value
; RAX += 0x87
; RBX -= 0x63
; RCX, RDX = RDX, RCX

; # Modify memory value
; MEM[RSP+0x0:RSP+0x4] += 0xdeadbeef
; MEM[RSP+0x4:RSP+0x8] -= 0xfaceb00c
; MEM[RSP+0x8:RSP+0xc], MEM[RSP+0xc:RSP+0x10] = MEM[RSP+0xc:RSP+0x10], MEM[RSP+0x8:RSP+0xc]

add rax, 0x87
sub rbx, 0x63

mov r8, rcx
mov rcx, rdx
mov rdx, r8

add dword [rsp], 0xdeadbeef
sub dword [rsp+0x4], 0xfaceb00c

mov r8d, dword [rsp+0x8]
mov r9d, dword [rsp+0xc]
mov dword [rsp+0x8], r9d
mov dword [rsp+0xc], r8d
