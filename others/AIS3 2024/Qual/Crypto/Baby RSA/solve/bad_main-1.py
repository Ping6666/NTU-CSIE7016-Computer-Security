# %%

from Crypto.Util.number import bytes_to_long, long_to_bytes

from sage.all import *

# ref
# ./hw1/coppersmith
# https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots
# https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense

# %%


def encrypt(m, e, n):
    enc = pow(bytes_to_long(m), e, n)
    return enc


# %%


def get_flag_builtin(n, e, ct, padding_shift, flag_size):
    """
    Args:
        flag_size: the absolute bound of the root (aka. the flag)

    """

    f_field = PolynomialRing(Zmod(n), names=('f_x', ))
    (f_x, ) = f_field._first_ngens(1)

    # x0 is a small root of f(x) = (a + x)3 - c (mod n)
    f_fn = (padding_shift + f_x)**e - ct

    # small_roots use the algo:
    #   Coppersmith’s algorithm for finding small roots using the LLL algorithm
    raw_flag = f_fn.small_roots(X=flag_size)

    return int(raw_flag[0])


# %%

from pwn import *

r = remote('chal1.eof.ais3.org', 10002)

res = r.recvline().strip().decode()

res = res.split(',')
n = int(res[0].split("=")[1])
e = int(res[1].split("=")[1])

r.recvuntil(b"FLAG:  ")
res = r.recvline().strip().decode()
ori_ct = int(res)

print(f"{n = }")
print(f"{e = }")
print(f"{ori_ct = }")
print()

flag_len = 8
padding = b"Padding in cryptography is a fundamental concept employed to ensure that data, typically in the form of plaintext, aligns properly with the encryption algorithm's block size. This process is crucial for symmetric block ciphers like AES and asymmetric encryption algorithms such as RSA. Padding involves adding extra bits to the input data before encryption, making it fit neatly into fixed-size blocks. The primary purpose of padding is to prevent information leakage by ensuring that the last block of plaintext is always complete, even when the original data's size isn't a perfect multiple of the block size. Common padding schemes include PKCS#7, PKCS#1 (for RSA), and ANSI X.923, each with its rules for padding and unpadding data. Proper padding ensures data integrity, security, and compatibility within cryptographic protocols."
my_flag = os.urandom(8)
print(f"{my_flag = }")

my_pt = padding + my_flag

my_ct = encrypt(my_pt, e, n)

print(f"{my_pt = }")
print(f"{my_ct = }")
print()

r.sendlineafter(b"Any message for me?", str(my_ct).encode())

# res = r.recvline().strip().decode()
# print(f"{res = }")

res = r.recvuntil(b"New Message: ")
res = r.recvline().strip().decode()

new_ct = int(res)

# %%

# absolute bound for the root (aka. the flag)
flag_size = 1 << (8 * flag_len)
padding_shift = bytes_to_long(padding) * flag_size

# %%

raw_flag_builtin = get_flag_builtin(n, e, new_ct, padding_shift, flag_size)

raw_flag = raw_flag_builtin
print("FLAG:", long_to_bytes(raw_flag))

# flag = b'FLAG{RandomPaddingIsImportant}'

# %%
