"""
_mm_store_si128((__m128i *)&v14, _mm_load_si128((const __m128i *)&xmmword_1400044D0));
_mm_store_si128((__m128i *)&v15, _mm_load_si128((const __m128i *)&xmmword_1400044E0));
_mm_store_si128((__m128i *)&v16, _mm_load_si128((const __m128i *)&xmmword_140004500));
_mm_store_si128((__m128i *)&v17, _mm_load_si128((const __m128i *)&xmmword_1400044F0));
_mm_store_si128((__m128i *)&v18, _mm_load_si128((const __m128i *)&xmmword_140004510));
v19 = 116;
v20 = 125;
_mm_store_si128((__m128i *)&v21, _mm_load_si128((const __m128i *)&xmmword_1400044A0));
_mm_store_si128((__m128i *)&v22, _mm_load_si128((const __m128i *)&xmmword_140004480));
_mm_store_si128((__m128i *)&v23, _mm_load_si128((const __m128i *)&xmmword_140004490));
_mm_store_si128((__m128i *)&v24, _mm_load_si128((const __m128i *)&xmmword_1400044C0));
_mm_store_si128((__m128i *)&v25, _mm_load_si128((const __m128i *)&xmmword_1400044B0));
v26 = 12;
v27 = 21;
"""

v1 = [
    0x46, 0x41, 0x31, 0x33, 0x34, 0x35, 0x4C, 0x47, 0x7B, 0x73, 0x6D, 0x6C,
    0x5F, 0x53, 0x4E, 0x5F, 0x63, 0x61, 0x70, 0x72, 0x74, 0x7D
]

# FA1345LG{sml_SN_caprt}

v2 = [
    0x00, 0x02, 0x06, 0x0A, 0x0E, 0x10, 0x01, 0x03, 0x04, 0x05, 0x07, 0x09,
    0x0B, 0x0F, 0x14, 0x11, 0x12, 0x13, 0x08, 0x0D, 0x0C, 0x15
]

flag = [''] * 22

for _v1, _v2 in zip(v1, v2):
    flag[int(_v2)] = chr(_v1)

flag = ''.join(flag)
print(f"{flag = }")
