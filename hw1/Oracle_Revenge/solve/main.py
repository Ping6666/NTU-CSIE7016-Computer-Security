# %%

from pwn import *

from random import randbytes

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes

# %%

block_size = 16

# %%


def pad(m):
    length = 16 - len(m) % 16
    return m + chr(length).encode() * length


# %%


def unpad(c):
    length = c[-1]
    for char in c[-length:]:
        if char != length:
            raise ValueError
    return c[:-length]


# %%


def asymmetric_encryption(message, n, e):
    # encrypt message with RSA
    # message must be 16 bytes
    # padding 100 bytes random value

    # padded_message = message
    padded_message = randbytes(100) + message
    return pow(bytes_to_long(padded_message), e, n)


# %%


def symmetric_encryption(message, key, iv=None):
    # ecrypt message with AES + CBC Mode
    # message can be arbitrary length

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(message))

    if iv is None:
        return cipher.iv, ct

    return ct


# %%


class SingletonRemote():
    conn: remote

    def __init__(self):
        self.conn = None
        return

    def cc_conn(self):
        try:
            self.conn.close()
            del self.conn

        except Exception as e:
            print("Closes the tube", e)

        self.conn = None
        return

    def init_conn(self):
        self.cc_conn()

        print("\nNew connection!!!")

        self.conn = remote('10.113.184.121', 10031)
        # self.conn = process(['python', './Alice_test.py'])
        return

    def solve_pad(self, enc_key, enc_iv, ct):

        while True:

            try:
                if not isinstance(self.conn, remote) and not isinstance(
                        self.conn, process):
                    raise TypeError

                self.conn.recvuntil(b"Give me the encrypted key: ")
                self.conn.sendline(str(enc_key).encode())

                self.conn.recvuntil(b"Give me the encrypted iv: ")
                self.conn.sendline(str(enc_iv).encode())

                self.conn.recvuntil(b"Give me the ciphertext: ")
                self.conn.sendline(bytes(ct).hex().encode())

                s = self.conn.recvline()

                if b"Bye~~" in s:
                    raise EOFError
                else:
                    break
            except KeyboardInterrupt:
                raise
            except:
                self.init_conn()

        return s


# %%


def padding_oracle_attack(sr: SingletonRemote,
                          n,
                          e,
                          enc_key,
                          iv,
                          ct,
                          verbose: bool = False):
    """
    Args:
        n: the N in RSA
        e: the e in RSA
        enc_key: the encrypted AES key
        iv: the initialization vector (16 bytes)
        ct: current CBC (Cipher-block chaining) ciphertext (16 bytes)

    """

    if len(iv) != block_size or len(ct) != block_size:
        print("POA length error!!")
        return b""

    pt = bytearray([0] * 16)

    # --- solve the block --- #

    # i: from block_size - 1 to 0
    for i in reversed(range(block_size)):

        # ii: from 0 to block_size - 1
        # ii + 1: curr padding
        ii = block_size - i - 1

        bf_iv = bytearray()
        bf_iv[:] = iv

        ## --- pad the iv --- ##

        # jj: from 0 to ii - 1
        for jj in range(ii):

            # j: from block_size - 1 to block_size - ii
            j = block_size - jj - 1

            bf_iv[j] = iv[j] ^ pt[j] ^ (ii + 1)

        ## --- brute force curr iv --- ##

        for bf in range(0, 256):
            print(f"\r{bf = :03d}  ", end='')

            bf_iv[i] = bf

            s = sr.solve_pad(enc_key, asymmetric_encryption(bf_iv, n, e), ct)

            if b"OK! Got it." in s:
                pt[i] = iv[i] ^ bf ^ (ii + 1)

                print(f"POA got {iv[i] = :03d}, {bf = :03d}," +
                      f" {ii + 1 = :02d}, {iv[i] ^ bf ^ (ii + 1) = :03d}.")
                break
        else:
            print(f"\n{bytes(pt) = }")
            print(f"Fail to solve with POA on" + f" {i = }, {ii + 1 = }.")
            return b""

        del bf_iv

    return bytes(pt)


# %%


def first_padding_oracle_attack(sr: SingletonRemote,
                                n,
                                e,
                                key,
                                enc_iv,
                                pt,
                                verbose: bool = False):
    """
    Args:
        n: the N in RSA
        e: the e in RSA
        key: the AES key (16 bytes)
        enc_iv: the encrypted initialization vector

    """

    enc_key = asymmetric_encryption(key, n, e)

    iv = bytearray([0] * 16)

    # --- solve the block --- #

    # i: from block_size - 1 to 0
    for i in reversed(range(block_size)):

        # ii: from 0 to block_size - 1
        # ii + 1: curr padding
        ii = block_size - i - 1

        bf_iv = bytearray()
        bf_iv[:] = iv

        ## --- pad the iv --- ##

        # jj: from 0 to ii - 1
        for jj in range(ii):

            # j: from block_size - 1 to block_size - ii
            j = block_size - jj - 1

            bf_iv[j] = iv[j] ^ (ii + 1)

        ## --- brute force curr iv --- ##

        for bf in range(0, 256):
            print(f"\r{bf = :03d}  ", end='')

            bf_iv[i] = bf

            bf_ct = symmetric_encryption(pt, key, bf_iv)
            s = sr.solve_pad(enc_key=enc_key,
                             enc_iv=enc_iv,
                             ct=bf_ct[:block_size])

            if b"OK! Got it." in s:
                iv[i] = bf_iv[i] ^ (ii + 1)

                print(f"POA got {bf_iv[i] = :03d}," +
                      f" {ii + 1 = :02d}, {bf_iv[i] ^ (ii + 1) = :03d}.")
                break
        else:
            print(f"\n{bytes(iv) = }")
            print(f"Fail to solve with POA on" + f" {i = }, {ii + 1 = }.")
            return b""

        del bf_iv

    return bytes(iv)


# %%

# RSA
oracle_N = 69214008498642035761243756357619851816607540327248468473247478342523127723748756926949706235406640562827724567100157104972969498385528097714986614165867074449238186426536742677816881849038677123630836686152379963670139334109846133566156815333584764063197379180877984670843831985941733688575703811651087495223
oracle_e = 65537

# encrypted
encrypted_flag = 67448907891721241368838325896320122397092733550961191069708016032244349188684070793897519352151466622385197077064799553157879456334546372809948272281247935498288157941438709402245513879910090372080411345199729220479271018326225319584057160895804120944126979515126944833368164622466123481816185794224793277249
encrypted_flag = int(encrypted_flag)

# %%

print(f"{oracle_N = }")
print(f"{oracle_e = }")
print(f"{encrypted_flag = }")
print()

# %%

# new_aes_key = os.urandom(16)
new_aes_key = b'\xa0\xd9\x99z\x1a9r}G\xe0\xbd\xa9=J\xe2\xe6'

print(f"{new_aes_key = }")

# %%

test_pt = b"Test"
pad_test_pt = pad(test_pt)

# %%

sr = SingletonRemote()

# %%

mod = pow(pow(2, 8), 16)
mod_inv = pow(mod, -1, oracle_N)

# %%

lsb = 0
sol_flag = b""

i = 0
while True:
    mod_inv_shift = pow(mod_inv, oracle_e * i, oracle_N)
    encrypted_flag_i = (encrypted_flag * mod_inv_shift) % oracle_N

    sol_iv = first_padding_oracle_attack(
        sr=sr,
        n=oracle_N,
        e=oracle_e,
        key=new_aes_key,
        enc_iv=encrypted_flag_i,
        pt=test_pt,
        verbose=False,
    )
    _lsb_byte = bytearray([
        _pad_test_pt ^ _sol_iv for _pad_test_pt, _sol_iv in zip(
            pad_test_pt[-block_size:], sol_iv[:block_size])
    ])
    _lsb = bytes_to_long(_lsb_byte)

    _flag_i = (_lsb - (lsb * mod_inv) % oracle_N) % mod
    lsb = (lsb * mod_inv + _flag_i) % oracle_N

    _flag_i_byte = long_to_bytes(_flag_i)

    print(f"{_flag_i_byte = }")
    print()

    sol_flag = _flag_i_byte + sol_flag

    if len(_flag_i_byte) != block_size:
        break

    i += 1

# %%

print(f"{sol_flag = }")
print()

# %%
