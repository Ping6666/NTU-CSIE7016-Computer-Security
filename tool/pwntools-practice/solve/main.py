from pwn import *

sys.setrecursionlimit(10010)


def qsort(arr: list):
    n = len(arr)
    if n == 0:
        return arr
    pivot = arr[n // 2]
    l = [i for i in arr if i < pivot]
    g = [i for i in arr if i > pivot]
    cnt = arr.count(pivot)

    assert len(l) == 0, "Bad pivot"

    return qsort(l) + [pivot] * cnt + qsort(g)


def inv_qsort(ins_num: int, arr: list):
    """
    Args:
        ins_num: need to be the smallest ele in the arr
    """

    n = (len(arr) + 1) // 2
    arr.insert(n, ins_num)

    return arr


def get_qsort_wc():
    """
    get the worst case of quicksort
    """

    _str, max_len = "0", 35000
    i, max_i = 0, -1
    while True:
        i += 1
        print(f"\ri {i:04d}  ", end='')
        if len(_str + " " + str(i)) > max_len:
            max_i = i
            break

        _str += " " + str(i)
    print()

    arr = []
    for i in reversed(range(max_i)):
        arr = inv_qsort(i, arr)

    qsort(arr)

    _str = ' '.join(str(i) for i in arr)

    return _str


rainbow_table = dict()


def build_rainbow_table(rate):
    print('rate', rate)

    _rand_range = int(2**24 * rate)
    for i in range(_rand_range):
        print(f"\r{i:08d}/{_rand_range:08d} ", end='')

        _h = hashlib.md5(f'{i}'.encode()).hexdigest()[0:8]
        _i = rainbow_table.get(_h)
        if _i is None:
            rainbow_table[_h] = i

    return


def main():

    _str = get_qsort_wc()
    print('get_qsort_wc done')

    # use rainbow table to prevent EOFError
    # set rate in order to reduce RAM usage

    rate = 0.25  # 1.0
    build_rainbow_table(rate=rate)
    print('\nbuild_rainbow_table done')

    counter = 0
    while True:
        counter += 1

        # should less than 20 times if rate=1.0
        print(f"\ntry times: {counter:02d}")

        try:
            # r = process(['python', '../src/main_1eef2d2606b37338.py'])
            r = remote('edu-ctf.csie.org', 54322)

            # ----- b'give me `i` such that md5(i)[0:8] == '

            s = r.recv()
            h = str(s).split('"')[1]
            print('hashlib.md5', h)

            correct_i = rainbow_table.get(h)
            if correct_i is None:
                r.close()
                continue

            print('correct i', correct_i)
            r.sendline(bytes(str(correct_i), encoding='utf-8'))

            # ----- b'your choice: '
            #   1 send a string that need to be sorted and complicated enough onto the server, and pass test_slow check.
            #   2 send a string match the regex, and pass test_slow check.
            #       the regex match is not slow enough
            #   3 need to compute proof_of_work 150 times per second, will send back a certificate and flag.
            #       pretty much impossible (or use rainbow table)

            s = r.recvuntil(b'your choice: ')
            r.sendline(bytes("1", encoding='utf-8'))

            # ----- b': '

            s = r.recvuntil(b': ')
            r.sendline(bytes(_str, encoding='utf-8'))

            s = r.recvall()
            if b'FLAG' in s or b'flag' in s:
                print(s)
                break
            else:
                print('No flag')

            r.close()

        except Exception as e:
            print("ERROR", e)

    return


if __name__ == '__main__':
    main()
