import numpy as np

a = 1
b = 0
tmp = -676742242
check = 0

state_fn = []

while not check:
    if tmp == -34633922:
        a = 13153783
        b = -385696007
        state_fn.append(0)

    elif tmp == -57059940:
        a = -292421353
        b = -369137459
        state_fn.append(1)

    elif tmp == -129301574:
        a = -1389871636
        b = -841441563
        state_fn.append(2)

    elif tmp == -164412249:
        a = -1946045638
        b = -166336692
        state_fn.append(3)

    elif tmp == -248361546:
        a = 1943305402
        b = 442242209
        state_fn.append(4)

    elif tmp == -268499918:
        a = 1240075617
        b = 1856824718
        state_fn.append(5)

    elif tmp == -286231349:
        a = -1657970905
        b = -520380403
        state_fn.append(6)

    elif tmp == -299036213:
        a = 362069224
        b = 48168843
        state_fn.append(7)

    elif tmp == -386052817:
        a = 1162602379
        b = 586032672
        state_fn.append(8)

    elif tmp == -387413440:
        a = -39139844
        b = 759028586
        state_fn.append(9)

    elif tmp == -393733339:
        a = 698416974
        b = -1226671529
        state_fn.append(10)

    elif tmp == -450612349:
        a = -1302315925
        b = -419326620
        state_fn.append(11)

    elif tmp == -638361507:
        a = -501600293
        b = 1064785757
        state_fn.append(12)

    elif tmp == -646963446:
        a = 1001524771
        b = -1225119943
        state_fn.append(13)

    elif tmp == -676742242:
        a = 1143581765
        b = 1267556787
        state_fn.append(14)

    elif tmp == -750472483:
        a = 1797380555
        b = -1101247860
        state_fn.append(15)

    elif tmp == -787123254:
        a = -546447420
        b = -509809256
        state_fn.append(16)

    elif tmp == -851605432:
        a = 918896919
        b = 1569686275
        state_fn.append(17)

    elif tmp == -874212301:
        a = 230425233
        b = 660326439
        state_fn.append(18)

    elif tmp == -1387842584:
        a = -1359671504
        b = -894885814
        state_fn.append(19)

    elif tmp == -1478133053:
        a = 2706084
        b = 1787887822
        state_fn.append(20)

    elif tmp == -1873424091:
        a = -1646006339
        b = 1181107551
        state_fn.append(21)

    elif tmp == -1921477935:
        a = 251248546
        b = -869636935
        state_fn.append(22)

    elif tmp == -1937726984:
        a = -412883775
        b = 1838856866
        state_fn.append(23)

    elif tmp == -1978223464:
        a = 514381144
        b = -42555480
        state_fn.append(24)

    elif tmp == -1985757190:
        a = -1227300782
        b = -744550629
        state_fn.append(25)

    elif tmp == -2031082028:
        a = -109950893
        b = -1492671614
        state_fn.append(26)

    elif tmp == -2092286981:
        a = 855390917
        b = 87293451
        state_fn.append(27)

    elif tmp == 2131447726:
        a = 2934436
        b = 1857704252
        state_fn.append(28)

    elif tmp == 2098792827:
        a = -1121234270
        b = 1729032134
        state_fn.append(29)

    elif tmp == 2095151013:
        a = 115055917
        b = 901530050
        state_fn.append(30)

    elif tmp == 2057902921:
        a = 19615453
        b = -546108769
        state_fn.append(31)

    elif tmp == 1978986903:
        a = 782269665
        b = -1269813824
        state_fn.append(32)

    elif tmp == 1929982570:
        a = -259885448
        b = -757938441
        state_fn.append(33)

    elif tmp == 1843624184:
        a = 813665441
        b = -481728723
        state_fn.append(34)

    elif tmp == 1780152111:
        a = -1376946450
        b = 1152243204
        state_fn.append(35)

    elif tmp == 1765279360:
        a = 1300239570
        b = 244578990
        state_fn.append(36)

    elif tmp == 1595228866:
        a = 96118341
        b = -719459762
        state_fn.append(37)

    elif tmp == 1438496410:
        a = -1503469500
        b = -36641556
        state_fn.append(38)

    elif tmp == 1154341356:
        a = 384462656
        b = 1100123695
        state_fn.append(39)

    elif tmp == 1132589236:
        a = -155208535
        b = 1357582708
        state_fn.append(40)

    elif tmp == 1093244921:
        a = -1217350874
        b = 565549260
        state_fn.append(41)

    elif tmp == 809393455:
        a = -2140063129
        b = 355890192
        state_fn.append(42)

    elif tmp == 794507810:
        a = 1324626540
        b = -576434528
        state_fn.append(43)

    elif tmp == 671274660:
        a = -808185822
        b = -1293557712
        state_fn.append(44)

    elif tmp == 557589375:
        a = 1345448523
        b = -1685776386
        state_fn.append(45)

    elif tmp == 416430256:
        a = 1409253995
        b = -444497599
        state_fn.append(46)

    elif tmp == 269727185:
        a = 576080139
        b = 1144229428
        state_fn.append(47)

    elif tmp == 71198295:
        a = -416569735
        b = -138126752
        state_fn.append(48)

    elif tmp == 126130845:
        a = -598538767
        b = 1283245962
        state_fn.append(49)

    else:
        check = 1

    tmp = np.int32(tmp)
    a = np.int32(a)
    b = np.int32(b)

    tmp = tmp * a + b

    # print(f"{tmp = }")

print(f"{state_fn = }")

# state_fn = [
#     14, 31, 44, 23, 38, 26, 0, 7, 11, 21, 46, 22, 27, 5, 36, 28, 40, 17, 29, 1,
#     47, 35, 4, 15, 6, 25, 8, 30, 20, 2, 12, 39, 42, 41, 37, 24, 19, 16, 9, 33,
#     3, 43, 34, 10, 49, 48, 45, 18, 13, 32
# ]
