from sage.rings.integer import Integer


def powmod(a, b):
    r = 1
    while b > 0:
        if b & 1:
            r = r * a
        a = a * a
        b >>= 1
    return r


print(powmod(Integer(11), Integer(3)))
