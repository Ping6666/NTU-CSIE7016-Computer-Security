# import sage

from functools import reduce
from Crypto.Util.number import long_to_bytes

# ref
# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# https://medium.com/analytics-vidhya/chinese-remainder-theorem-using-python-25f051e391fc


def get_crt(mods, remains):
    """
    Chinese Remainder Theorem
    """

    sum = 0
    mul_mod = reduce(lambda _mul, _m: _mul * _m, mods)

    for _m, _r in zip(mods, remains):
        _mul_mod = mul_mod // _m
        sum += _r * get_mod_mul_inv(_mul_mod, _m) * _mul_mod

    return sum % mul_mod


def get_mod_mul_inv(mul, mod):
    ori_mod = mod
    x0, x1 = 0, 1  # prev_mod_mul_inv, curr_mod_mul_inv

    if mod == 1:
        return 1

    while mul > 1:
        _mul = mul // mod
        mul, mod = mod, mul % mod

        x0, x1 = x1 - _mul * x0, x0

    if x1 < 0:
        x1 += ori_mod

    return x1


def inv_xorrrrr(nums):
    """
    aka. xorrrrr
    """

    n = len(nums)
    result = [0] * n

    for i in range(1, n):
        result = [result[j] ^ nums[(j + i) % n] for j in range(n)]

        # --- sage --- #
        # result = [result[j] ^^ nums[(j + i) % n] for j in range(n)]

    return result


def main():

    hint = [
        297901710, 2438499757, 172983774, 2611781033, 2766983357, 1018346993,
        810270522, 2334480195, 154508735, 1066271428, 3716430041, 875123909,
        2664535551, 2193044963, 2538833821, 2856583708, 3081106896, 2195167145,
        2811407927, 3794168460
    ]
    muls = [
        865741, 631045, 970663, 575787, 597689, 791331, 594479, 857481, 797931,
        1006437, 661791, 681453, 963397, 667371, 705405, 684177, 736827,
        757871, 698753, 841555
    ]
    mods = [
        2529754263, 4081964537, 2817833411, 3840103391, 3698869687, 3524873305,
        2420253753, 2950766353, 3160043859, 2341042647, 4125137273, 3875984107,
        4079282409, 2753416889, 2778711505, 3667413387, 4187196169, 3489959487,
        2756285845, 3925748705
    ]

    print(f"hint = {hint}")
    print(f"muls = {muls}")
    print(f"mods = {mods}")
    print()

    ori_hint = inv_xorrrrr(hint)
    ori_muls = inv_xorrrrr(muls)
    ori_mods = inv_xorrrrr(mods)

    print(f"ori_hint = {ori_hint}")
    print(f"ori_muls = {ori_muls}")
    print(f"ori_mods = {ori_mods}")
    print()

    inv_mods = [-1] * 20
    new_hint = [-1] * 20

    for i in range(20):
        inv_mods[i] = get_mod_mul_inv(ori_muls[i], ori_mods[i])
        new_hint[i] = ori_hint[i] * inv_mods[i] % ori_mods[i]

    # --- sage --- #
    # for i in range(20):
    #     inv_mods[i] = sage.arith.misc.inverse_mod(ori_muls[i], ori_mods[i])
    #     new_hint[i] = ori_hint[i] * inv_mods[i] % ori_mods[i]

    print(f"inv_mods = {inv_mods}")
    print(f"new_hint = {new_hint}")
    print()

    _secret = get_crt(ori_mods, new_hint)
    _bytes_secret = long_to_bytes(_secret)

    # --- sage --- #
    # _secret = sage.arith.misc.CRT(new_hint, ori_mods)
    # _bytes_secret = long_to_bytes(_secret)

    print(f"secret = {_secret}")
    print(f"bytes_secret = {_bytes_secret}")
    print()

    return


if __name__ == '__main__':
    main()
