# %%
from pwn import *
from sage.all import *

from Crypto.Util.number import long_to_bytes

# ref
# https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.CRT_list
# https://owasp.org/www-pdf-archive/Practical_Invalid_Curve_Attacks_on_TLS-ECDH_-_Juraj_Somorovsky.pdf
# https://crypto.stackexchange.com/questions/71065/invalid-curve-attack-finding-low-order-points
# https://www.hackthebox.com/blog/business-ctf-2022-400-curves-write-up
# https://github.com/p4-team/ctf/tree/master/2019-04-07-spam-and-flags-teaser/crypto_ecc
# http://the2702.com/2015/05/08/invalid-curve-attack.html

# %%
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

# %%
print(f"{p = }")
print(f"{a = }")
print(f"{b = }")
print(f"{n = }")
print()

# %%


def invalid_curve_attack(_p,
                         _a,
                         _b,
                         lower_bound=pow(2, 10),
                         upper_bound=pow(2, 30),
                         verbose: bool = False):
    ec = EllipticCurve(Zmod(_p), [_a, _b])
    _order = ec.order()
    _factors = prime_factors(_order)

    if verbose:
        print(f"{_factors = }")

    hints = []
    mods = []

    for _prime in _factors:

        # skip large subgroups
        if _prime > lower_bound and _prime < upper_bound:

            try:
                if verbose:
                    print(f"{_prime = }")

                g = ec.gen(0) * int(_order / _prime)

                if verbose:
                    print("Point G", g)

                ## --- start of interactive --- ##
                # r = process(['python', './invalid_curve_attack_test.py'])
                r = remote('10.113.184.121', 10034)

                r.sendlineafter(b"Gx: ", str(g[0]).encode())
                r.sendlineafter(b"Gy: ", str(g[1]).encode())

                hint_x, hint_y = eval(r.recvall().decode().strip())
                r.close()
                ## --- end of interactive --- ##

                h = ec(hint_x, hint_y)

                if verbose:
                    print("Point H", h)
                    print("\nDiscrete log...")

                _hint = g.discrete_log(h)

                if verbose:
                    print(f"{_hint = }")
                    print()

                hints.append(_hint)
                mods.append(_prime)

            except KeyboardInterrupt:
                return [], []

            except:
                # bad point
                pass

    return hints, mods


# %%

the_flag = b""

hints = []
mods = []

i = 0
while True:
    i += 1
    print("\n\n\n########################################")
    print("Hint count:", i)

    try:
        curve_b = randint(1, p)
        _hints, _mods = invalid_curve_attack(p, a, curve_b)

        hints.extend(_hints)
        mods.extend(_mods)

        _flag = CRT(hints, mods)
        the_flag = long_to_bytes(_flag)
        print(f"FLAG = {the_flag}")

        if b"FLAG" in the_flag or b"flag" in the_flag:
            break

    except KeyboardInterrupt:
        break

    except:
        # bad curve
        pass

# %%
print(f"\n\n\nFLAG = {the_flag}")

# FLAG = b'FLAG{YouAreARealECDLPMaster}'

# %%
