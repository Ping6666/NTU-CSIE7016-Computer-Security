import numpy as np


def next_tmp(t, a, b):
    t = np.int32(t)
    a = np.int32(a)
    b = np.int32(b)

    t = t * a + b
    return t


a = 1
b = 0
tmp = -676742242
check = 0

state_fn = []

while not check:
    check = 1

    if tmp == -34633922:
        a = 13153783
        b = -385696007
        state_fn.append(0)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xFDEF873E):
        continue

    if tmp == -57059940:
        a = -292421353
        b = -369137459
        state_fn.append(1)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xFC99559C):
        continue

    if tmp == -129301574:
        a = -1389871636
        b = -841441563
        state_fn.append(2)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xF84B03BA):
        continue

    if tmp == -164412249:
        a = -1946045638
        b = -166336692
        state_fn.append(3)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xF63344A7):
        continue

    if tmp == -248361546:
        a = 1943305402
        b = 442242209
        state_fn.append(4)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xF1324DB6):
        continue

    if tmp == -268499918:
        a = 1240075617
        b = 1856824718
        state_fn.append(5)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xEFFF0432):
        continue

    if tmp == -286231349:
        a = -1657970905
        b = -520380403
        state_fn.append(6)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xEEF074CB):
        continue

    if tmp == -299036213:
        a = 362069224
        b = 48168843
        state_fn.append(7)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xEE2D11CB):
        continue

    if tmp == -386052817:
        a = 1162602379
        b = 586032672
        state_fn.append(8)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xE8FD4D2F):
        continue

    if tmp == -387413440:
        a = -39139844
        b = 759028586
        state_fn.append(9)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xE8E88A40):
        continue

    if tmp == -393733339:
        a = 698416974
        b = -1226671529
        state_fn.append(10)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xE8E88A40):
        continue

    if tmp == -450612349:
        a = -1302315925
        b = -419326620
        state_fn.append(11)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xE5243383):
        continue

    if tmp == -638361507:
        a = -501600293
        b = 1064785757
        state_fn.append(12)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xD9F3605D):
        continue

    if tmp == -646963446:
        a = 1001524771
        b = -1225119943
        state_fn.append(13)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xD9701F0A):
        continue

    if tmp == -676742242:
        a = 1143581765
        b = 1267556787
        state_fn.append(14)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xD7A9BB9E):
        continue

    if tmp == -750472483:
        a = 1797380555
        b = -1101247860
        state_fn.append(15)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xD344B2DD):
        continue

    if tmp == -787123254:
        a = -546447420
        b = -509809256
        state_fn.append(16)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xD11573CA):
        continue

    if tmp == -851605432:
        a = 918896919
        b = 1569686275
        state_fn.append(17)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xCD3D8848):
        continue

    if tmp == -874212301:
        a = 230425233
        b = 660326439
        state_fn.append(18)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xCBE49433):
        continue

    if tmp == -1387842584:
        a = -1359671504
        b = -894885814
        state_fn.append(19)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xAD4733E8):
        continue

    if tmp == -1478133053:
        a = 2706084
        b = 1787887822
        state_fn.append(20)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0xA7E57AC3):
        continue

    if tmp == -1873424091:
        a = -1646006339
        b = 1181107551
        state_fn.append(21)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x9055D125):
        continue

    if tmp == -1921477935:
        a = 251248546
        b = -869636935
        state_fn.append(22)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x8D7892D1):
        continue

    if tmp == -1937726984:
        a = -412883775
        b = 1838856866
        state_fn.append(23)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x8C80A1F8):
        continue

    if tmp == -1978223464:
        a = 514381144
        b = -42555480
        state_fn.append(24)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x8A16B498):
        continue

    if tmp == -1985757190:
        a = -1227300782
        b = -744550629
        state_fn.append(25)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x89A3BFFA):
        continue

    if tmp == -2031082028:
        a = -109950893
        b = -1492671614
        state_fn.append(26)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x86F025D4):
        continue

    if tmp == -2092286981:
        a = 855390917
        b = 87293451
        state_fn.append(27)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x834A3BFB):
        continue

    if tmp == 2131447726:
        a = 2934436
        b = 1857704252
        state_fn.append(28)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x7F0B4FAE):
        continue

    if tmp == 2098792827:
        a = -1121234270
        b = 1729032134
        state_fn.append(29)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x7D19097B):
        continue

    if tmp == 2095151013:
        a = 115055917
        b = 901530050
        state_fn.append(30)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x7CE177A5):
        continue

    if tmp == 2057902921:
        a = 19615453
        b = -546108769
        state_fn.append(31)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x7AA91B49):
        continue

    if tmp == 1978986903:
        a = 782269665
        b = -1269813824
        state_fn.append(32)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x75F4F197):
        continue

    if tmp == 1929982570:
        a = -259885448
        b = -757938441
        state_fn.append(33)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x7309326A):
        continue

    if tmp == 1843624184:
        a = 813665441
        b = -481728723
        state_fn.append(34)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x6DE378F8):
        continue

    if tmp == 1780152111:
        a = -1376946450
        b = 1152243204
        state_fn.append(35)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x6A1AF72F):
        continue

    if tmp == 1765279360:
        a = 1300239570
        b = 244578990
        state_fn.append(36)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x69380680):
        continue

    if tmp == 1595228866:
        a = 96118341
        b = -719459762
        state_fn.append(37)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x5F1542C2):
        continue

    if tmp == 1438496410:
        a = -1503469500
        b = -36641556
        state_fn.append(38)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x55BDB69A):
        continue

    if tmp == 1154341356:
        a = 384462656
        b = 1100123695
        state_fn.append(39)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x44CDD9EC):
        continue

    if tmp == 1132589236:
        a = -155208535
        b = 1357582708
        state_fn.append(40)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x4381F0B4):
        continue

    if tmp == 1093244921:
        a = -1217350874
        b = 565549260
        state_fn.append(41)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x412997F9):
        continue

    if tmp == 809393455:
        a = -2140063129
        b = 355890192
        state_fn.append(42)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x303E5D2F):
        continue

    if tmp == 794507810:
        a = 1324626540
        b = -576434528
        state_fn.append(43)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x2F5B3A22):
        continue

    if tmp == 671274660:
        a = -808185822
        b = -1293557712
        state_fn.append(44)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x2802D6A4):
        continue

    if tmp == 557589375:
        a = 1345448523
        b = -1685776386
        state_fn.append(45)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x213C237F):
        continue

    if tmp == 416430256:
        a = 1409253995
        b = -444497599
        state_fn.append(46)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x18D238B0):
        continue

    if tmp == 269727185:
        a = 576080139
        b = 1144229428
        state_fn.append(47)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp > np.int32(0x1013B5D1):
        continue

    if tmp == 71198295:
        a = -416569735
        b = -138126752
        state_fn.append(48)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

    if tmp == 126130845:
        a = -598538767
        b = 1283245962
        state_fn.append(49)
        check = 0
        tmp = next_tmp(tmp, a, b)
        continue

print(f"{state_fn = }")

# state_fn = [
#     14, 31, 44, 23, 38, 26, 0, 7, 11, 21, 46, 22, 27, 5, 36, 28, 40, 17, 29, 1,
#     47, 35, 4, 15, 6, 25, 8, 30, 20, 2, 12, 39, 42, 41, 37, 24, 19, 16, 9, 33,
#     3, 43, 34, 10, 49, 48, 45, 18, 13, 32
# ]
