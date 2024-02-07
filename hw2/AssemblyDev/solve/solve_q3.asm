; Challenge Info

; let a = MEM[RSP+0x0:RSP+0x4]
; let b = MEM[RSP+0x4:RSP+0x8]
; let c = MEM[RSP+0x8:RSP+0xc]
; let d = MEM[RSP+0xc:RSP+0x10]

; # a, b -> signed 4 btyes integer
; if a >= b:
;     EAX = a
; else:
;     EAX = b

; # c, d -> unsigned 4 btyes integer
; if c < d:
;     EBX = c
; else:
;     EBX = d

; if c is an odd number:
;     ECX = c // 8
; else:
;     ECX = c * 4

mov r8d, dword [rsp]
mov r9d, dword [rsp+0x4]

cmp r8d, r9d

jl l10  ; else
mov eax, r8d
jmp l11

l10:
mov eax, r9d

l11:


mov r8d, dword [rsp+0x8]
mov r9d, dword [rsp+0xc]

cmp r8d, r9d

jae l20  ; else
mov ebx, r8d
jmp l21

l20:
mov ebx, r9d

l21:


mov r8d, eax
mov eax, dword [rsp+0x8]
mov edx, 0

test eax, 1

jz l30  ; else
mov r9d, 8
div r9d
jmp l31

l30:
mov r9d, 4
mul r9d

l31:
mov ecx, eax
mov eax, r8d
