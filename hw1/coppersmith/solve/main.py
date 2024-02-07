# %%

from Crypto.Util.number import bytes_to_long, long_to_bytes

from sage.all import *

# ref
# https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots
# https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense

# %%


def get_flag_builtin(n, e, ct, padding_shift, flag_size):
    """
    Args:
        flag_size: the absolute bound of the root (aka. the flag)

    """

    f_field = PolynomialRing(Zmod(n), names=('f_x', ))
    (f_x, ) = f_field._first_ngens(1)

    # x0 is a small root of f(x) = (a + x)3 - c (mod n)
    f_fn = (padding_shift + f_x)**e - ct

    # small_roots use the algo:
    #   Coppersmith’s algorithm for finding small roots using the LLL algorithm
    raw_flag = f_fn.small_roots(X=flag_size)

    return int(raw_flag[0])


def get_flag_coppersmith(n, e, ct, padding_shift, flag_size):
    """
    Args:
        flag_size: the absolute bound of the root (aka. the flag)
        
    """

    # Coppersmith’s Method, RSA - Stereotyped Messages

    a = padding_shift
    r = flag_size

    coef = [
        [r**3, (e * a * (r**2)), (e * pow(a, e - 1) * r), (pow(a, e) - ct)],
        [0, n * (r**2), 0, 0],
        [0, 0, n * r, 0],
        [0, 0, 0, n],
    ]
    martix = Matrix(coef)

    # Return LLL reduced or approximated LLL reduced lattice for this matrix interpreted as a lattice.
    l = martix.LLL()

    # get a lattice
    v = l[0]

    # integer field
    f_field = PolynomialRing(ZZ, names=('f_x', ))
    (f_x, ) = f_field._first_ngens(1)

    # built a polynomial from the shortest coefficient vector (aka. the lattice above)
    f_fn = ((v[0] // (r**3)) * (f_x**3) + (v[1] // (r**2)) * (f_x**2) +
            (v[2] // (r**1)) * (f_x**1) + v[3])

    raw_flag = f_fn.roots()

    return int(raw_flag[0][0])


# %%

e = 3
n = 11548249006448728920152703839381630946834097081458641312395741399152626808167055308830597218237419306363812953570976143239712039037941209800604194908083149885941768218371746741812573578768412807189143962911312361667909189521442378332430658999991458388376075547304981934158525694587528155624390264161508298680598416212224037418377397597560818727159266535257243347737195812548494888452510974912762585150695881388036715559552242157015756455473208463066542053661043988897316002396230791287157322382659981842882278113445574922266102197380093864871418103716702341116793118630092030597784102701252267617442078055768183287429
ct = 10016669153906644953016660527326048255337800602435656916304698358749910229624738375584073093905785564737742726549033330343901680652357648652891913260149958947299067801907769873568759955053120633017158582128001396334187309835478967775943564724073809481988489791896725867047366927584419210464759674986336704398037888892734158765679221980466827060998749130113847401820986980535379266905587107992796676977541915779320084736207068268591500847603252838325486939367980604888710370629644796971859833251926677637185722683564847418746350226830775205063128441515048529918173084258483536354002888691012853231754416802134513394608

flag_len = 30
padding = b"Padding in cryptography is a fundamental concept employed to ensure that data, typically in the form of plaintext, aligns properly with the encryption algorithm's block size. This process is crucial for symmetric block ciphers like AES and asymmetric encryption algorithms such as RSA. Padding involves adding extra bits to the input data before encryption, making it fit neatly into fixed-size blocks. The primary purpose of padding is to prevent information leakage by ensuring that the last block of plaintext is always complete, even when the original data's size isn't a perfect multiple of the block size. Common padding schemes include PKCS#7, PKCS#1 (for RSA), and ANSI X.923, each with its rules for padding and unpadding data. Proper padding ensures data integrity, security, and compatibility within cryptographic protocols."

# %%

# absolute bound for the root (aka. the flag)
flag_size = 1 << (8 * 30)
padding_shift = bytes_to_long(padding) * flag_size

# %%

raw_flag_coppersmith = get_flag_coppersmith(n, e, ct, padding_shift, flag_size)
raw_flag_builtin = get_flag_builtin(n, e, ct, padding_shift, flag_size)

if raw_flag_coppersmith != raw_flag_builtin:
    print("Wrong Answer!!!")
else:
    raw_flag = raw_flag_builtin
    print("FLAG:", long_to_bytes(raw_flag))

# flag = b'FLAG{RandomPaddingIsImportant}'

# %%
