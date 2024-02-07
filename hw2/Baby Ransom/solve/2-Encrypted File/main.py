from Crypto.Cipher import ARC4

filename = './robots.txt'
_txts = open(filename, 'r').read()

_bytes = [ord(_t) for _t in _txts[2687:2706]]

print(len(_txts))
print(_txts[2687:2706])
print(_bytes)

for _b in _bytes:
    print(f"{_b:02x}", end=' ')

# /72833139015/orders
# 2f 37 32 38 33 33 31 33 39 30 31 35 2f 6f 72 64 65 72 73

print("\n")

filename = './enc_flag.txt'
_flag_bytes = open(filename, 'rb').read()

print(len(_flag_bytes))
print(_flag_bytes)

for _b in _flag_bytes:
    print(f"{_b:02x}", end=' ')

# 71 04 1f c7 93 1a 7c a0 e1 f5 08 44 d0 08 18 d7 1d e0 22 b5 a3 ad 3a c9 b2 d5 e7 40 41 4b 86 97 e8 2e 6b

print("\n")

_len = 8  # len('flag.txt')
key = bytes(_bytes)[:_len]

cipher = ARC4.new(key)
msg = cipher.decrypt(_flag_bytes)

print(msg)

# b'FLAG{50_y0u_p4y_7h3_r4n50m?!hmmmmm}'
