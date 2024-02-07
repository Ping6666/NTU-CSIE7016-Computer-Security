# %%
from itertools import combinations

from Crypto.Util.number import long_to_bytes


# %%
class LFSR:
    """
    Stream cipher
    linear-feedback shift register
    """

    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x


# %%
def correlation_attacks(tap,
                        seq_len: int,
                        stream,
                        bits_len: int,
                        correlation: float = 0.7):
    """
    Args:
        tap: the tap in LSFR
        seq_len: the length of the state in LSFR
        stream: is the stream ciphers

    """

    counter = 0

    for l in range(seq_len):
        for c in combinations(range(seq_len), l):
            print(f"\r{counter:07d} ", end='')
            counter += 1

            # flip the bit if selected
            _stream = [
                1 - stream[i] if i in c else stream[i] for i in range(seq_len)
            ]
            _lfsr = LFSR(tap, _stream)
            _lfsr_bits = [_lfsr.getbit() for _ in range(bits_len)]

            match_num = sum(a == b for (a, b) in zip(stream, _lfsr_bits))

            if match_num >= correlation * bits_len:
                print("\nGot you!!!", _stream)
                return _stream

    return None


# %%
def brute_force_attack(tap, seq_len, lfsr2_stream, lfsr3_stream, stream,
                       bits_len: int):

    for _state in range(1 << seq_len):
        print(f"\r{_state:07d} ", end='')

        state = [int(i) for i in f"{_state:019b}"]
        _lfsr = LFSR(tap, state)

        checker = True
        for i in range(bits_len):
            s = lfsr2_stream[i] if _lfsr.getbit() else lfsr3_stream[i]
            if s != stream[i]:
                checker = False
                break

        if checker:
            print("\nGot you!!!", state)
            return state

    return None


# %%
tap = [0, 1, 2, 5]
stream = [
    0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1,
    1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0,
    1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0,
    1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0,
    0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1,
    1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
    0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
    0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0,
    1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0,
    1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1,
    1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0,
    1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0
]
bits_len = 200

# %%
states_lfsr2 = correlation_attacks(tap, 23, stream, bits_len)
states_lfsr3 = correlation_attacks(tap, 27, stream, bits_len)

lfsr2 = LFSR(tap, states_lfsr2)
lfsr3 = LFSR(tap, states_lfsr3)

lfsr2_stream = [lfsr2.getbit() for _ in stream]
lfsr3_stream = [lfsr3.getbit() for _ in stream]

# %%
states_lfsr1 = brute_force_attack(tap, 19, lfsr2_stream, lfsr3_stream, stream,
                                  bits_len)

lfsr1 = LFSR(tap, states_lfsr1)

lfsr1_stream = [lfsr1.getbit() for _ in stream]

# %%
_flag = [
    s ^ (s2 if s1 else s3)
    for s, s1, s2, s3 in zip(stream, lfsr1_stream, lfsr2_stream, lfsr3_stream)
]
flag = long_to_bytes(int("".join(map(str, _flag[bits_len:])), 2))
print("flag", flag)
