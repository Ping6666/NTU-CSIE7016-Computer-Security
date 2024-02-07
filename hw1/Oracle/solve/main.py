# %%

from multiprocessing import Pool

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

    def __del__(self):
        self.cc_conn()
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


def padding_oracle_attack(n,
                          e,
                          enc_key,
                          iv,
                          ct,
                          bf_start=0,
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

    sr = SingletonRemote()

    pt = bytearray([0] * 16)

    # --- solve the block --- #

    # i: from block_size - 1 to 0
    for i in reversed(range(block_size)):
        if i != (block_size - 1):
            bf_start = 0

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

        for bf in range(bf_start, 256):
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

            bf_start = pt[15] ^ iv[15] ^ (1) + 1
            if bf_start != 256:

                print(f"Retry other possibilities")
                return padding_oracle_attack(n,
                                             e,
                                             enc_key,
                                             iv,
                                             ct,
                                             bf_start=bf_start,
                                             verbose=verbose)

            return b""

        del bf_iv

    return bytes(pt)


# %%


def first_padding_oracle_attack(n, e, key, enc_iv, pt, verbose: bool = False):
    """
    Args:
        n: the N in RSA
        e: the e in RSA
        key: the AES key (16 bytes)
        enc_iv: the encrypted initialization vector

    """

    sr = SingletonRemote()

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
###########################################

# %%

# RSA
oracle_N = 69214008498642035761243756357619851816607540327248468473247478342523127723748756926949706235406640562827724567100157104972969498385528097714986614165867074449238186426536742677816881849038677123630836686152379963670139334109846133566156815333584764063197379180877984670843831985941733688575703811651087495223
oracle_e = 65537

# encrypted_info
oracle_encrypted_key = 65690013242775728459842109842683020587149462096059598501313133592635945234121561534622365974927219223034823754673718159579772056712404749324225325531206903216411508240699572153162745754564955215041783396329242482406426376133687186983187563217156659178000486342335478915053049498619169740534463504372971359692
oracle_encrypted_iv = 35154524936059729204581782839781987236407179504895959653768093617367549802652967862418906182387861924584809825831862791349195432705129622783580000716829283234184762744224095175044663151370869751957952842383581513986293064879608592662677541628813345923397286253057417592725291925603753086190402107943880261658

# encrypted_flag
file_name = '../src/encrypted_flag_d6fbfd5306695c4a.not_png'

oracle_ct = open(file_name, 'rb').read()
oracle_ct = bytearray(oracle_ct)

# %%

# new_aes_key = os.urandom(16)
new_aes_key = b'\xa0\xd9\x99z\x1a9r}G\xe0\xbd\xa9=J\xe2\xe6'

print(f"{new_aes_key = }")

# %%

test_pt = b"Test"
pad_test_pt = pad(test_pt)

# %%

sol_iv = first_padding_oracle_attack(
    n=oracle_N,
    e=oracle_e,
    key=new_aes_key,
    enc_iv=oracle_encrypted_iv,
    pt=test_pt,
    verbose=False,
)

real_iv = bytearray(
    [f ^ s for f, s in zip(pad_test_pt[-block_size:], sol_iv[:block_size])])
# real_iv = b'K\xa3\xcb\x1c\x13FQ\xc3\xbb\\\xd6\xe3\x81\xc2\x90\x9b'

# %%

print(f"{real_iv = }")
print()

# %%

# recover the original ct
oracle_ct = real_iv + oracle_ct

# %%
############################################

# %%

oracle_ct_len = len(oracle_ct)
oracle_ct_b_len = oracle_ct_len // block_size  # 2391 + 1

# %%

print(f"{oracle_ct_len = }")
print(f"{oracle_ct_b_len = }")
print()

# %%

pool = Pool(processes=24)

# %%

map_iterable = []
for i in range(oracle_ct_b_len):
    _iterable = (oracle_N, oracle_e, oracle_encrypted_key,
                 oracle_ct[i * block_size:(i + 1) * block_size],
                 oracle_ct[(i + 1) * block_size:(i + 2) * block_size])
    map_iterable.append(_iterable)

# %%

pool_outputs = pool.starmap(padding_oracle_attack, map_iterable)

pool.close()
pool.join()

# %%

print(pool_outputs)

# %%

flag_png = b"".join(pool_outputs)

# %%

open('./flag.png', 'wb').write(flag_png)

# %%

# FLAG{Rea11yu5efu110rac1eisntit?}

# %%
