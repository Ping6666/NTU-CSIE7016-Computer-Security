filename = './rsrc_68'
_bytes = open(filename, 'rb').read()

_xor = bytearray([0x11, 0x87])

_dll = bytearray([])

for i in range(len(_bytes)):
    _byte = _bytes[i] ^ _xor[i % 2]
    _dll.append(_byte)

open('payload', 'wb').write(_dll)

# certutil -hashfile ./payload md5

# flag: FLAG{e6b77096375bcff4c8bc765e599fbbc0}
