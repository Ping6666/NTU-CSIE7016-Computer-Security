def _ror(val, bits, bit_size):
    return ((val & (2 ** bit_size - 1)) >> bits % bit_size) | \
        ((val << (bit_size - (bits % bit_size))) & (2 ** bit_size - 1))


def magic_fn(data: bytearray):
    """
    v12_data = _data;
    v2_len = _len;
    v3 = 0xE0C92EAB;
    memset(Dst, 0, 0x400u);
    v4_data_idx = 0;
    if ( v2_len )
    {
        v5 = v12_data - (_DWORD)Dst;
        v13 = v12_data - (_DWORD)Dst;
        do
        {
            v6 = v3 ^ Dst[v4_data_idx + v5];        // v6 = v3 ^ _data[v4_data_idx]
                                                    //
            Dst[v4_data_idx] = v6;
            v3 = v2_len + (v6 ^ __ROR4__(v3, 3)) - v4_data_idx;
            Sleep(0x3E8u);
            printf_15C0(std::cout, &unk_403418);    // printf('.')
                                                    //
            v5 = v13;
            ++v4_data_idx;
        }
        while ( v4_data_idx < v2_len );
    }
    """

    _magic = 0xE0C92EAB

    data_len = len(data)

    tmp_len = 1024
    tmp = [0] * tmp_len

    _len = min(data_len, tmp_len)

    for i in range(_len):
        _tmp = _magic ^ data[i]
        tmp[i] = _tmp
        _magic = data_len + (_tmp ^ _ror(_magic, 3, 32)) - i

    return tmp


def inv_magic_fn(dst: bytearray):

    _magic = 0xE0C92EAB

    _len = len(dst) - 1
    data = [0] * _len

    for i in range(_len):
        _tmp = dst[i]
        data[i] = _tmp ^ _magic & 0xFF
        _magic = _len + (_tmp ^ _ror(_magic, 3, 32)) - i

    return data


# unk_403400
filename = './dst.txt'
dst = open(filename, 'rb').read()

print(len(dst))
print(f"{dst = }")

data = inv_magic_fn(dst)

print(f"{data = }")

flag = ''.join(chr(_data) for _data in data)

print(f"{flag = }")
print()
