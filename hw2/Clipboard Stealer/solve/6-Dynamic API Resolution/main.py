def _rol(val, bits, bit_size):
    return (val << bits % bit_size) & (2 ** bit_size - 1) | \
           ((val & (2 ** bit_size - 1)) >> (bit_size - (bits % bit_size)))


user32 = open('./user32.dll.txt', 'r').readlines()

for name in user32:
    name = name.strip()

    _tmp = 0
    for i in name:
        _tmp += _rol(_tmp, 11, 32) + 1187 + ord(i)

    if _tmp % (1 << 32) == 0x416f607:
        print("FLAG{" + name + "}")
        break
else:
    print("Fail to find api in user32.dll")
