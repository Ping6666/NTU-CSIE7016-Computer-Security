#include <stdio.h>
#include <stdint.h>

int main()
{
    // for (i = 0; i < a2; ++i)
    // {
    //     v5 = byte_2020[i];
    //     s1[i] = v5 ^ a3;
    //     a3 = a2 - i + (v5 ^ __ROR4__(a3, 1));
    // }

    uint8_t bytes[] = {0x4a, 0x3c, 0x66, 0xd0, 0xc7, 0x4b, 0xc6, 0xb7, 0x1b, 0x0d,
                       0xc0, 0x56, 0xb8, 0xd7, 0xd3, 0x47, 0xb4, 0xe6, 0x67, 0x0e,
                       0xb6, 0x50, 0x92, 0x8c, 0x22, 0x5c, 0x63, 0x8b, 0x07, 0x09,
                       0xf6, 0xf1, 0x64, 0x8a, 0x8b, 0xf2, 0x00, 0x00, 0x00, 0x00};
    uint8_t s[36];

    int n = 0x24;
    uint64_t secret = 0xbaceb00c;

    for (int i = 0; i < n; i++)
    {
        uint8_t b = bytes[i];

        s[i] = (uint8_t)secret ^ b;
        secret = ((secret >> 1 | (uint64_t)((secret & 1) != 0) << 0x1f) ^ (uint64_t)b) + (n - i);

        printf("%c", s[i]);
    }
    printf("\n\n");

    return 0;
}
