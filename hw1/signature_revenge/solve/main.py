# %%

from hashlib import sha256

from ecdsa import SECP256k1

from Crypto.Util.number import bytes_to_long, long_to_bytes

from sage.all import *

# %%


def get_flag(n, s1, s2, h1, h2, inv_r1, inv_r2, a, l):

    def get_d(s, inv_r, h, k):
        return int(((k * s - h) * inv_r) % n)

    m1 = -l[0] % n
    m2 = l[1] % n

    k1 = m1 * a + m2
    k2 = m2 * a + m1

    k1_d = get_d(s1, inv_r1, h1, k1)
    k2_d = get_d(s2, inv_r2, h2, k2)

    if k1_d != k2_d:
        return False, None

    return True, long_to_bytes(k1_d)


# %%

ec = SECP256k1
g, n = ec.generator, ec.order

# p = dg
p = (
    70427896289635684269185763735464004880272487387417064603929487585697794861713,
    83106938517126976838986116917338443942453391221542116900720022828358221631968
)

# signed with k1
sig1 = (
    26150478759659181410183574739595997895638116875172347795980556499925372918857,
    50639168022751577246163934860133616960953696675993100806612269138066992704236
)
# signed with k2
sig2 = (
    8256687378196792904669428303872036025324883507048772044875872623403155644190,
    90323515158120328162524865800363952831516312527470472160064097576156608261906
)

# %%

r1, s1 = sig1
h1 = sha256(b"https://www.youtube.com/watch?v=IBnrn2pnPG8").digest()
h1 = bytes_to_long(h1)

r2, s2 = sig2
h2 = sha256(b"https://www.youtube.com/watch?v=1H2cyhWYXrE").digest()
h2 = bytes_to_long(h2)

# %%

# t = -s1 -1 s2 r1 r2 -1
# u = s1 -1 r1 h2 r2 -1 - s1 -1 h1
# k1 + tk2 + u ≡ 0 mod n

inv_s1 = pow(s1, -1, n)
inv_r1 = pow(r1, -1, n)
inv_r2 = pow(r2, -1, n)

t = Zmod(n)(-1 * (inv_s1 * s2 * r1 * inv_r2))
u = Zmod(n)((inv_s1 * r1 * h2 * inv_r2) - (inv_s1 * h1))

print(f"{t = }")
print(f"{u = }")
print()

# %%

a = 1 << (8 * 16)
k = 1 << (8 * 16)

convert_t = (1 + a * t) / (a + t)
convert_u = u / (a + t)

print(f"{convert_t = }")
print(f"{convert_u = }")
print()

# %%

coef = [
    [n, 0, 0],
    [convert_t, 1, 0],
    [convert_u, 0, k],
]
martix = Matrix(ZZ, coef)

# Return LLL reduced or approximated LLL reduced lattice for this matrix interpreted as a lattice.
l = martix.LLL()

print(l)
print()

# %%

lattices = [
    l[0],
    l[1],
    l[2],
    l[0] + l[1],
    l[0] + l[2],
    l[1] + l[2],
    l[0] + l[1] + l[2],
    # ...
]

for l in lattices:
    ret, flag = get_flag(n, s1, s2, h1, h2, inv_r1, inv_r2, a, l)

    if ret:
        if b"FLAG" in flag or b"flag" in flag:
            print(f"{flag = }")
            break

# %%
