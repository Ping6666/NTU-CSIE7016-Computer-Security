# %%

import numpy as np

# %%


def state(id, state):
    if id == 0:
        # state_4260333374
        state[16] += (state[11] + state[25])
    elif id == 1:
        # state_4237907356
        state[19] += (state[10] + state[16])
    elif id == 2:
        # state_4165665722
        state[13] += (state[25] + state[28])
    elif id == 3:
        # state_4130555047
        state[4] += (state[25] + state[27])
    elif id == 4:
        # state_4046605750
        state[24] += (state[5] + state[20])
    elif id == 5:
        # state_4026467378
        state[39] -= (state[25] + state[38])
    elif id == 6:
        # state_4008735947
        state[1] += (state[6] + state[15])
    elif id == 7:
        # state_3995931083
        state[31] += (state[16] + state[34])
    elif id == 8:
        # state_3908914479
        state[1] += (state[16] + state[40])
    elif id == 9:
        # state_3907553856
        state[41] -= (state[3] + state[34])
    elif id == 10:
        # state_3901233957
        state[10] -= (state[12] + state[22])
    elif id == 11:
        # state_3844354947
        state[9] += (state[3] + state[11])
    elif id == 12:
        # state_3656605789
        state[7] += (state[0] + state[10])
    elif id == 13:
        # state_3648003850
        state[8] += (state[14] + state[16])
    elif id == 14:
        # state_3618225054
        state[14] += (state[8] + state[35])
    elif id == 15:
        # state_3544494813
        state[7] += (state[0] + state[21])
    elif id == 16:
        # state_3507844042
        state[13] += (state[8] + state[26])
    elif id == 17:
        # state_3443361864
        state[30] -= (state[8] + state[33])
    elif id == 18:
        # state_3420754995
        state[17] += (state[24] + state[38])
    elif id == 19:
        # state_2907124712
        state[2] += (state[25] + state[34])
    elif id == 20:
        # state_2816834243
        state[32] += (state[5] + state[25])
    elif id == 21:
        # state_2421543205
        state[17] += (state[0] + state[7])
    elif id == 22:
        # state_2373489361
        state[37] -= (state[3] + state[29])
    elif id == 23:
        # state_2357240312
        state[2] += (state[8] + state[11])
    elif id == 24:
        # state_2316743832
        state[0] += (state[28] + state[31])
    elif id == 25:
        # state_2309210106
        state[30] -= (state[2] + state[13])
    elif id == 26:
        # state_2263885268
        state[14] -= (state[6] + state[32])
    elif id == 27:
        # state_2202680315
        state[23] += (state[7] + state[34])
    elif id == 28:
        # state_2131447726
        state[20] += (state[19] + state[24])
    elif id == 29:
        # state_2098792827
        state[1] -= (state[13] + state[29])
    elif id == 30:
        # state_2095151013
        state[31] += (state[1] + state[16])
    elif id == 31:
        # state_2057902921
        state[9] -= (state[2] + state[22])
    elif id == 32:
        # state_1978986903
        state[5] += (state[20] + state[37])
    elif id == 33:
        # state_1929982570
        state[37] += (state[18] + state[27])
    elif id == 34:
        # state_1843624184
        state[18] += (state[26] + state[31])
    elif id == 35:
        # state_1780152111
        state[36] += (state[11] + state[15])
    elif id == 36:
        # state_1765279360
        state[27] += (state[18] + state[20])
    elif id == 37:
        # state_1595228866
        state[4] += (state[7] + state[25])
    elif id == 38:
        # state_1438496410
        state[6] += (state[10] + state[41])
    elif id == 39:
        # state_1154341356
        state[21] += (state[15] + state[34])
    elif id == 40:
        # state_1132589236
        state[15] += (state[10] + state[22])
    elif id == 41:
        # state_1093244921
        state[18] += (state[15] + state[29])
    elif id == 42:
        # state_809393455
        state[21] -= (state[13] + state[42])
    elif id == 43:
        # state_794507810
        state[23] += (state[30] + state[39])
    elif id == 44:
        # state_671274660
        state[0] = state[0] - state[18] + state[31]
    elif id == 45:
        # state_557589375
        state[15] += (state[8] + state[40])
    elif id == 46:
        # state_416430256
        state[5] += (state[4] + state[40])
    elif id == 47:
        # state_269727185
        state[0] += (state[16] + state[33])
    elif id == 48:
        # state_71198295
        state[37] += (state[12] + state[16])
    elif id == 49:
        # state_126130845
        state[4] += (state[6] + state[22])

    # ---------- #

    elif id == 50:
        # state_637380471 (unused)
        state[13] += (state[16] + state[29])

    return state


def inv_state(id, state):
    if id == 0:
        # state_4260333374
        # state[16] += (state[11] + state[25])
        state[16] -= (state[11] + state[25])
    elif id == 1:
        # state_4237907356
        # state[19] += (state[10] + state[16])
        state[19] -= (state[10] + state[16])
    elif id == 2:
        # state_4165665722
        # state[13] += (state[25] + state[28])
        state[13] -= (state[25] + state[28])
    elif id == 3:
        # state_4130555047
        # state[4] += (state[25] + state[27])
        state[4] -= (state[25] + state[27])
    elif id == 4:
        # state_4046605750
        # state[24] += (state[5] + state[20])
        state[24] -= (state[5] + state[20])
    elif id == 5:
        # state_4026467378
        # state[39] -= (state[25] + state[38])
        state[39] += (state[25] + state[38])
    elif id == 6:
        # state_4008735947
        # state[1] += (state[6] + state[15])
        state[1] -= (state[6] + state[15])
    elif id == 7:
        # state_3995931083
        # state[31] += (state[16] + state[34])
        state[31] -= (state[16] + state[34])
    elif id == 8:
        # state_3908914479
        # state[1] += (state[16] + state[40])
        state[1] -= (state[16] + state[40])
    elif id == 9:
        # state_3907553856
        # state[41] -= (state[3] + state[34])
        state[41] += (state[3] + state[34])
    elif id == 10:
        # state_3901233957
        # state[10] -= (state[12] + state[22])
        state[10] += (state[12] + state[22])
    elif id == 11:
        # state_3844354947
        # state[9] += (state[3] + state[11])
        state[9] -= (state[3] + state[11])
    elif id == 12:
        # state_3656605789
        # state[7] += (state[0] + state[10])
        state[7] -= (state[0] + state[10])
    elif id == 13:
        # state_3648003850
        # state[8] += (state[14] + state[16])
        state[8] -= (state[14] + state[16])
    elif id == 14:
        # state_3618225054
        # state[14] += (state[8] + state[35])
        state[14] -= (state[8] + state[35])
    elif id == 15:
        # state_3544494813
        # state[7] += (state[0] + state[21])
        state[7] -= (state[0] + state[21])
    elif id == 16:
        # state_3507844042
        # state[13] += (state[8] + state[26])
        state[13] -= (state[8] + state[26])
    elif id == 17:
        # state_3443361864
        # state[30] -= (state[8] + state[33])
        state[30] += (state[8] + state[33])
    elif id == 18:
        # state_3420754995
        # state[17] += (state[24] + state[38])
        state[17] -= (state[24] + state[38])
    elif id == 19:
        # state_2907124712
        # state[2] += (state[25] + state[34])
        state[2] -= (state[25] + state[34])
    elif id == 20:
        # state_2816834243
        # state[32] += (state[5] + state[25])
        state[32] -= (state[5] + state[25])
    elif id == 21:
        # state_2421543205
        # state[17] += (state[0] + state[7])
        state[17] -= (state[0] + state[7])
    elif id == 22:
        # state_2373489361
        # state[37] -= (state[3] + state[29])
        state[37] += (state[3] + state[29])
    elif id == 23:
        # state_2357240312
        # state[2] += (state[8] + state[11])
        state[2] -= (state[8] + state[11])
    elif id == 24:
        # state_2316743832
        # state[0] += (state[28] + state[31])
        state[0] -= (state[28] + state[31])
    elif id == 25:
        # state_2309210106
        # state[30] -= (state[2] + state[13])
        state[30] += (state[2] + state[13])
    elif id == 26:
        # state_2263885268
        # state[14] -= (state[6] + state[32])
        state[14] += (state[6] + state[32])
    elif id == 27:
        # state_2202680315
        # state[23] += (state[7] + state[34])
        state[23] -= (state[7] + state[34])
    elif id == 28:
        # state_2131447726
        # state[20] += (state[19] + state[24])
        state[20] -= (state[19] + state[24])
    elif id == 29:
        # state_2098792827
        # state[1] -= (state[13] + state[29])
        state[1] += (state[13] + state[29])
    elif id == 30:
        # state_2095151013
        # state[31] += (state[1] + state[16])
        state[31] -= (state[1] + state[16])
    elif id == 31:
        # state_2057902921
        # state[9] -= (state[2] + state[22])
        state[9] += (state[2] + state[22])
    elif id == 32:
        # state_1978986903
        # state[5] += (state[20] + state[37])
        state[5] -= (state[20] + state[37])
    elif id == 33:
        # state_1929982570
        # state[37] += (state[18] + state[27])
        state[37] -= (state[18] + state[27])
    elif id == 34:
        # state_1843624184
        # state[18] += (state[26] + state[31])
        state[18] -= (state[26] + state[31])
    elif id == 35:
        # state_1780152111
        # state[36] += (state[11] + state[15])
        state[36] -= (state[11] + state[15])
    elif id == 36:
        # state_1765279360
        # state[27] += (state[18] + state[20])
        state[27] -= (state[18] + state[20])
    elif id == 37:
        # state_1595228866
        # state[4] += (state[7] + state[25])
        state[4] -= (state[7] + state[25])
    elif id == 38:
        # state_1438496410
        # state[6] += (state[10] + state[41])
        state[6] -= (state[10] + state[41])
    elif id == 39:
        # state_1154341356
        # state[21] += (state[15] + state[34])
        state[21] -= (state[15] + state[34])
    elif id == 40:
        # state_1132589236
        # state[15] += (state[10] + state[22])
        state[15] -= (state[10] + state[22])
    elif id == 41:
        # state_1093244921
        # state[18] += (state[15] + state[29])
        state[18] -= (state[15] + state[29])
    elif id == 42:
        # state_809393455
        # state[21] -= (state[13] + state[42])
        state[21] += (state[13] + state[42])
    elif id == 43:
        # state_794507810
        # state[23] += (state[30] + state[39])
        state[23] -= (state[30] + state[39])
    elif id == 44:
        # state_671274660
        # state[0] = state[0] - state[18] + state[31]
        state[0] = state[0] + state[18] - state[31]
    elif id == 45:
        # state_557589375
        # state[15] += (state[8] + state[40])
        state[15] -= (state[8] + state[40])
    elif id == 46:
        # state_416430256
        # state[5] += (state[4] + state[40])
        state[5] -= (state[4] + state[40])
    elif id == 47:
        # state_269727185
        # state[0] += (state[16] + state[33])
        state[0] -= (state[16] + state[33])
    elif id == 48:
        # state_71198295
        # state[37] += (state[12] + state[16])
        state[37] -= (state[12] + state[16])
    elif id == 49:
        # state_126130845
        # state[4] += (state[6] + state[22])
        state[4] -= (state[6] + state[22])

    # ---------- #

    elif id == 50:
        # state_637380471 (unused)
        # state[13] += (state[16] + state[29])
        state[13] -= (state[16] + state[29])

    else:
        raise NotImplementedError

    return state


# %%

state_fn = [
    14, 31, 44, 23, 38, 26, 0, 7, 11, 21, 46, 22, 27, 5, 36, 28, 40, 17, 29, 1,
    47, 35, 4, 15, 6, 25, 8, 30, 20, 2, 12, 39, 42, 41, 37, 24, 19, 16, 9, 33,
    3, 43, 34, 10, 49, 48, 45, 18, 13, 32
]

target = [
    0xD5, 0x4B, 0xEC, 0x33, 0x06, 0x55, 0xF4, 0x1A, 0x3C, 0x42, 0x65, 0x75,
    0x5F, 0xC4, 0xA2, 0xD3, 0x3B, 0xAD, 0xBC, 0xB0, 0xDB, 0x54, 0x6C, 0xE0,
    0x2B, 0x72, 0x5F, 0x2D, 0x54, 0x61, 0x49, 0x79, 0xDE, 0x65, 0x53, 0x24,
    0xE3, 0x5A, 0x74, 0x80, 0x65, 0xCC, 0x7D
]
# target = [
#     213, 75, 236, 51, 6, 85, 244, 26, 60, 66, 101, 117, 95, 196, 162, 211, 59,
#     173, 188, 176, 219, 84, 108, 224, 43, 114, 95, 45, 84, 97, 73, 121, 222,
#     101, 83, 36, 227, 90, 116, 128, 101, 204, 125
# ]

target = np.uint8(target)
print(f"{target}")

for _id in reversed(state_fn):
    # target = state(_id, target)
    target = inv_state(_id, target)

print(f"{target}")

for t in target:
    try:
        print(chr(t), end="")
    except:
        print(hex(t))
        print("AAA")

print()
