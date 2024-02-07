def fn_magic(fn_name: str):
    """
    signed __int64 __fastcall get_fn_magic_2810(_BYTE *a1)
    {
      unsigned __int64 v1; // ST00_8
      signed __int64 v3; // [rsp+0h] [rbp-18h]
      _BYTE *v4; // [rsp+20h] [rbp+8h]

      v4 = a1;
      v3 = 0xCBF29CE484222325i64;
      while ( *v4 )
      {
        v1 = (char)*v4++ ^ (unsigned __int64)v3;
        v3 = 0x100000001B3i64 * v1;
      }
      return v3;
    }
    """

    magic = 0xCBF29CE484222325
    for i in fn_name:
        magic = 0x100000001B3 * (ord(i) ^ magic)

    return magic % (1 << 64)


filenames = [
    './dlls/kernel32.dll.txt',
    './dlls/msvcrt.dll.txt',
    './dlls/user32.dll.txt',
    './dlls/wininet.dll.txt',
]

txt_files = [open(_name, 'r').readlines() for _name in filenames]

fn_magic_nums = [
    [
        0x69D265FE6B1C110F, 0x578960F1FC7FFF25, 0xFA55E32C9D72A921,
        0xE0746E00B47C0477, 0xE7BDCAD1F3AE0E13, 0x1C71D0537E2246F5,
        0x121E523CBB49F938, 0x1C8EF920B632E586, 0x28D0403A889E4F69,
        0x556A045B10DE85, 0x2E97865AB85128C3, 0x2FA16C1D95E4306A,
        0x5D35AEBEDFD88117, 0xFC59546FD0D3D778, 0xEBC4E8E9B1542DEE
    ],
    [
        0x974ADB99DCFF7A24,
        0xD9C0619DA0F59BAD,
        0x2AB2847890E35C03,
    ],
    [
        0x1E307D27BA21DDA4,
    ],
    [
        0x8261F0DF5FDC0887,
        0xE726A35A86C7641C,
        0x6F4E79C87F04F3E6,
        0x2DF8494D5C13046,
    ],
]

for filename, _txt, _fn_magic in zip(filenames, txt_files, fn_magic_nums):

    for _name in _txt:
        _magic = fn_magic(_name.strip())

        if _magic in _fn_magic:
            print(filename, _name, hex(_magic))
    print()
