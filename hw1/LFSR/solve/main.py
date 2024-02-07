# %%
from sage.all import *

import numpy as np

# ref
# https://www.embeddedrelated.com/showarticle/1114.php
# https://stackoverflow.com/questions/9509502/in-python-how-do-you-convert-8-bit-binary-numbers-into-their-ascii-characters

# %%
state_len = 64
taps = [0, 2, 17, 19, 23, 37, 41, 53]
taps_arr = [1 if i in taps else 0 for i in range(state_len)]

# %%
pad = np.zeros((state_len, state_len - 1), dtype=int)
taps_np_arr = np.array([taps_arr], dtype=int).reshape(-1, 1)

cm_array = np.eye(state_len, k=-1, dtype=int)
cm_array += np.concatenate([pad, taps_np_arr], axis=1)

# %%
print(cm_array)

# %%
output = [
    0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1,
    1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1,
    0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0,
    0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1,
    0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1,
    1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0,
    1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1,
    0
]

output_len = len(output)  # 326
flag_len = output_len - 70  # 256

# %%
print(output_len)
print(flag_len)

# %%
cm = Matrix(cm_array)
cm_71 = cm**(70 + 1)  # inner loop times

# %%
print(cm)
print(cm_71)

# %%
cm_base = Matrix(GF(2), 64)
cm_71_shift = cm_71**(flag_len + (70 - 64))

for i in range(64):
    cm_71_shift = cm_71_shift * cm_71
    cm_base[i] = cm_71_shift[0]

# %%
back_ouput = output[-64:]
back_state = vector(GF(2), back_ouput)

ori_state = (cm_base**-1) * back_state

# %%
print('back_state', back_state)
print('ori_state', ori_state)

# %%

p_state = ori_state

flag_str = ""
raw_str = ""

for i in range(flag_len):
    c_state = cm_71 * p_state

    _str = int(c_state[0]) ^ output[i]
    raw_str += str(_str)

    if len(raw_str) == 8:
        flag_str += chr(int(raw_str, 2))
        raw_str = ""

    p_state = c_state

print("flag", flag_str)

# %%
