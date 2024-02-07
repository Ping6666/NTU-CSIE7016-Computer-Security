; Challenge Info

; let a = MEM[RSP+0x0:RSP+0x4]
; let b = MEM[RSP+0x4:RSP+0x8]
; let c = MEM[RSP+0x8:RSP+0xc]

; EAX = a + b
; EBX = a - b
; ECX = -c
; EDX = 9*a + 7

mov eax, dword [rsp]         ; a
mov ebx, 9

mul ebx
add eax, 7
mov edx, eax

mov ecx, dword [rsp + 0x8]   ; c

neg ecx

mov eax, dword [rsp]         ; a
mov ebx, dword [rsp]         ; a

mov r8d, dword [rsp + 0x4]   ; b

add eax, r8d
sub ebx, r8d
