# HW1

## \[Lab\] COR

- Flag: `FLAG{Corre1ati0n_Attack!_!}`

### 解題過程 & 思路

1. 題目使用 19+23+27 bits 操作 LFSR (Linear feedback shift register)，但是卻沒有如此程度的安全性。
    
    $$2^{69} \rightarrow 2^{19} + 2^{23} + 2^{27}$$
    
2. 因此可以使用真值表的性質 (75% correlated) 以達到 correlation attacks，如此可以解出 `x2` & `x3`；另因為 LFSR 的計算過程有 200 bits，所以使得 correlation attacks 相對容易解出。
3. 解出 `x2` & `x3` 後便可以暴搜出 `x1`，因為 `x1` 只有 $2^{19}$ 種可能，並不會大到不切實際，所以直接暴搜所有可能，直到透過 `x2 if x1 else x3` get bit 的輸出能與原始 stream 完全一致。
4. 還原出 `x1` & `x2` & `x3` 就可以還原出 flag。

> Flag

![](/pic/hw1/1.png)

## \[Lab\] POA

- Flag: `FLAG{pAdd1NG_0rAcL3_A77aCK}\x00\x00\x00\x00`

### 解題過程 & 思路

1. server 會對 padding 做檢查，因此能夠使用 AES CBC mode Xor 的性質，操作 iv 以達到 Bit-flipping attack 的效果，所以只要能夠塞入正確 padding，便能還原出原本的明文。
2. 實作 padding oracle attack，對於每個 block 依序實作，其中對於每個 block，從後面的 byte 開始依序向前方的 byte 操作，計算當前的 padding，如果 server 能 unpad，透過 xor 還原出目前位置原本的明文。

> Flag

![](/pic/hw1/2.png)

## \[Lab\] LSB

- Flag: `FLAG{Viycx_qsklsjgmeld_fgd_spkgjo}`

### 解題過程 & 思路

1. server 會幫忙解密輸入的數字，雖然只有回傳 `mod 3` 後的結果，但是這樣就足夠還原出原本的明文了。
2. 透過性質將數字分解成: $x_n, x_{n-1}, ..., x_2, x_1, x_0$，在與 server 互動的過程可以藉由 `pt % 3` 結果，依序地知道序列中的數值， 如此便能夠還原出原本的明文。

> Flag

![](/pic/hw1/3.png)

## \[HW1\] LFSR

- Flag: `FLAG{Lf5r_15_50_eZZzZzZZZzzZzzz}`

### 解題過程 & 思路

1. LFSR 對 register 所做的操作看似複雜，其實本質上就是 matrix 的操作，在數學上也就是線性代數的 companion matrix，由於 `taps` 是已知的資訊，所以 companion matrix 也是已知的資訊。
2. 雖然題目中每 71 次操作 (get bit) 只有 1 次有記錄下來，但是因為 companion matrix 是已知的資訊，所以如果有超過 64 bits 原始 output 便能夠還原出原本的 initial state。
3. 因為 output 有 70 bits 不受到 flag 影響，所以能夠透過這些 bits & companion matrix 還原出 initial state，如此便能求出 flag。
4. 首先，透過 `taps` 建構出 companion matrix 作為 `cm` (如下方 code block)，因為 71 次操作才記錄 1 次，所以需要計算出 `cm_71 = cm**(70 + 1)`。
5. 接者，需要透過 output 後方與 flag 無關的 bits 與 `cm_base**-1` 還原出原本的 initial state，`cm_base` 為 initial state 與 output 的轉移矩陣，此時因為不同位置的 output bit 雖然都是從相同的 initial state 轉移過來，但是其受到 `cm_71` 矩陣操作的次數不同，因此建構 `cm_base` 的方式則是對於每個 output bit idx 不同，計算 `cm_71**(bit idx)` 依序填入。
6. 求出 `cm_base` 後便能夠還原出 initial state，也就能夠還原出受到 flag xor 前的 output stream 與 flag。

> Reference

1. [Linear Feedback Shift Registers for the Uninitiated, Part VIII: Matrix Methods and State Recovery - Jason Sachs](https://www.embeddedrelated.com/showarticle/1114.php)
2. [In Python, how do you convert 8-bit binary numbers into their ASCII characters? - Stack Overflow](https://stackoverflow.com/questions/9509502/in-python-how-do-you-convert-8-bit-binary-numbers-into-their-ascii-characters)

> Flag

![](/pic/hw1/4.png)

## \[HW1\] Oracle

- Flag: `FLAG{Rea11yu5efu110rac1eisntit?}`

### 解題過程 & 思路

1. 這題可以使用基本的 POA (Padding Oracle Attack)，使用 $`{ct}_{i-1}`$ & $`{ct}_{i}`$ 還原出 $`{pt}_{i}`$。
    1. 如下圖，可以透過原本的 $key$ 與已知的 $`{ct}_{i-1}`$ & $`{ct}_{i}`$ 作為 $iv$ & $ct$ 帶入，便能夠透過兩個已知的資訊求出一個未知的 $pt$。
2. 但是 $`{pt}_{0}`$ 需要 $iv$ 才能夠解出，可是題目中的 $iv$ 卻已經被加密了，所以需要先解出 $iv$ 才能利用基本的 POA 還原出 $`{pt}_{0}`$。
    1. 如下圖，由於只有一個已知的資訊，這樣不足以推出兩個未知的資訊。
    2. 不過其實第一個 block (first 16 bytes) 就是 PNG magic number，其中第一個 block 的前 8 bytes 是 PNG file signature，後 8 bytes 是 IHDR chunk 描述符，所以在這題其實可以不用解出 $iv$。
3. 但是觀察下圖與 server 的行為，發現可以藉由操控 $key$ 與其 $iv$ 使得 $ct$ & $pt$ 是已知的兩個資訊，如此便能先求出 $iv$ 這一個未知的資訊；求得 $iv$ 後，便能夠回到第一點基本的 POA 已順利求出 $`{pt}_{0}`$
    
![](/pic/hw1/13.svg)
    
4. $iv$: 實作 first padding oracle attack，給入已知的 `key`, `enc_iv`與一個先假設好的 `pt`，過程中計算 `enc_key` 與藉由改變 `bf_iv` 計算出 `ct`，以提供給 server 解密與 unpad。不過這樣只能還原出 `pt ^ iv`，所以最後還需要使用已知的 `pt` 還原出 `iv`。
5. $pt$: 有了 $iv$ 便能夠使用基本的 POA 還原出整串 `pt`，不過遇到一些問題需要修正，如下:
    1. 如果對於第一個 `pt` 假設 padding 是 `0x01`，有 0.5%~1% 的 block 會猜錯最後一個 byte padding (每個 block 中第一個嘗試的 byte)，所以便對這部分出了修正，如果解不出此 block 前面的 byte，便回到最後一個 byte 重新檢查 padding。
    2. 還有因為 block 數量實在太多了，一個一個 block 來解太慢了，好在 AES CBC mode 使得解出來的 `pt` 相互獨立、互不影響，所以可以用多線程來解決，~~只好用 DOS 來解決~~。
6. 搞定 $pt$ 也就搞定 `flag.png`，如此也就順利求出 flag 了。

> Reference

1. [PNG Specification: File Structure](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)

> Flag

![](/pic/hw1/5.png)

## \[HW1\] Oracle_Revenge

- Flag: `FLAG{Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_Oo_oracle_of_oracle_oO_oO_o_oO_oO_o_oO_oO_o_oO_oO_o_oO_oO_o_oO_oO}`

### 解題觀察 & 思路

1. 原先以為要利用 RSA 的一些性質解開 `d`，如此再還原出 flag。
2. 後來想想因為 $iv$ (aka. `encrypted_flag`) 可以受到控制，而 block_size 是由 AES 決定且固定的，因此可以結合 POA 與 LSB 的方法，將一個一個 block 的 flag 還原出來。
3. 參考上述於 LSB 與 POA 與 Oracle 的解法，調整 LSB 中的 `mod` 變成 block_size: $2^{8 \times 16}$，如此便能還原出 flag。

> Flag

![](/pic/hw1/6.png)

## \[Lab\] dlog

- Flag: `FLAG{YouAreARealRealRealRealDiscreteLogMaster}`

### 解題過程 & 思路

1. 存在 prime number `p`，根據性質 `Zmod(p)` 的 order 為 `p - 1`，如果說 `p` 很 smooth 則表示 `p - 1` 可以輕易的被分解。
2. 所以可以由小的質數建構出 `p - 1`，檢查 `p` 是 prime 後拿此數值去跟 server 互動。
3. 最後因為 `p` 足夠 smooth，所以能透過 `discrete_log` 還原出 flag。

> Flag

![](/pic/hw1/7.png)

## \[Lab\] signature

- Flag: `FLAG{EphemeralKeyShouldBeRandom}`

### 解題過程 & 思路

1. 當 `k` 的挑選不隨機時，便能夠還原出 `d`。
    
    $$k_1 = {s_1}^{-1} H_1 + d \times ({s_1}^{-1} r_1) \mod q$$
    $$k_2 = {s_2}^{-1} H_2 + d \times ({s_2}^{-1} r_2) \mod q$$
    $$d = ({s_1}^{-1} H_1 - {s_2}^{-1} H_2) \ / \ ({s_2}^{-1} r_2 - {s_1}^{-1} r_1)$$
    
2. 還原出 `d` 後，就能透過私鑰簽章、通過驗章檢查，如此便能拿到 flag。

> Flag

![](/pic/hw1/8.png)

## \[Lab\] coppersmith

- Flag: `FLAG{RandomPaddingIsImportant}`

### 解題過程 & 思路

1. 已知 padding 與 flag 的長度 (upper bound)，可以用 Coppersmith’s Method & Lenstra–Lenstra–Lovász Algorithm 判斷能否求出方程式的根。
2. 可以用 sagemath 內建的方法，給定方程式求根，演算法一樣是 LLL；也可以自己建構正確的 matrix，求出 shortest vector。

> Reference

1. [Dense univariate polynomials over \(\ZZ/n\ZZ\), implemented using NTL - Polynomials](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots)
2. [Dense matrices over the integer ring - Matrices and Spaces of Matrices](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html#sage.matrix.matrix_integer_dense.Matrix_integer_dense)

> Flag

![](/pic/hw1/9.png)

## \[HW1\] invalid_curve_attack

- Flag: `FLAG{YouAreARealECDLPMaster}`

### 解題過程 & 思路

1. 這題很有趣，原本以為是要用數學性質找到一個非常非常非常 smooth 的 Elliptic Curve。
2. 雖然投影片有提及，但是查了許多資料才真正了解 Elliptic Curve order 的意義。那就是任何於 Elliptic Curve 上的 Point，乘上 order 後會繞回到相同的 Point，因為這個乘法性質，使得 a, b 成立。
    1. $H = P \times (order \ / \ n) \times Flag = G \times Flag$
    2. $hint = G.discretelog(H) = Flag \mod n$
3. 這樣就簡化了問題，不需要找到非常非常非常 smooth 的 Elliptic Curve，只需要找到相對 smooth 的 EllipticCurve，重現 Elliptic Curve 的乘法性質，嘗試不同的 Elliptic Curve 與不同的起始 Point。
4. 如此便能分解出不算太大的 n (aka. prime number in the factor of Elliptic Curve order)，接者使用 discrete log 求解找出 hint，當有足夠多個 hint & prime，就可以使用 CRT 還原出 flag。

> Reference

1. [Miscellaneous arithmetic functions - Standard Commutative Rings](https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.CRT_list)
2. [OWASP - Practical Invalid Curve Attacks on TLS-ECDH](https://owasp.org/www-pdf-archive/Practical_Invalid_Curve_Attacks_on_TLS-ECDH_-_Juraj_Somorovsky.pdf)
3. [diffie hellman - Invalid curve attack: finding low order points - Cryptography Stack Exchange](https://crypto.stackexchange.com/questions/71065/invalid-curve-attack-finding-low-order-points)
4. [Business CTF 2022: Invalid curve attack - 400 Curves](https://www.hackthebox.com/blog/business-ctf-2022-400-curves-write-up)
5. [ctf/2019-04-07-spam-and-flags-teaser/crypto_ecc at master · p4-team/ctf](https://github.com/p4-team/ctf/tree/master/2019-04-07-spam-and-flags-teaser/crypto_ecc)
6. [The 2702 - Computer Security and CTF Writeups](http://the2702.com/2015/05/08/invalid-curve-attack.html)

> Flag

![](/pic/hw1/10.png)

## \[HW1\] signature_revenge

- Flag: `FLAG{LLLisreaLLyusefuL}`

### 解題過程 & 思路

1. 此題雖然可以使用 lattice basis 與 LLL 來解出 shortest vector，但是 $k_1, k_2$ 的大小並不符合 constrain。
    
    $$\;Let \;t = - {s_1}^{-1} s_2 r_1 {s_2}^{-1}, u = {s_1}^{-1} r_1 h_2 {r_2}^{-1} - {s_1}^{-1} h_1$$
    $$k_1 + t k_2 + u = 0 \mod n$$
    
2. 仔細觀察後，發現 ${m}_1, {m}_2$ 的 upper bound 能夠符合 constrain，所以需要先將 $k_1, k_2$ 以 ${m}_1, {m}_2$ 表示 (here $m$ stand for magic)，如此能夠建構出 matrix 並解出 shortest vector。
    
    $$\;Let \;a = 2 ^ {8 \times 16}$$
    $$(m_1 \times a + m_2) + t (m_2 \times a + m_1) + u = 0 \mod n$$
    $$constrain: |m_1|, |m_2| < K = 2^{8 \times 16} \leq n^{1/2}$$
    
3. 解出 shortest vectors 也就是解出 ${m}_1, {m}_2$ 後，便能組合出 $k_1, k_2$，並透過 $k_1, k_2$ 推算出 $d$，但此時推算出的 $d$ 並非 flag。
4. 這是因為此題所有可能的解就好比是在一個環上面，matrix 透過 LLL 所解出的 shortest vectors 可能是位於環上的位置 or 在環上的步長，所以需要透過這些 vector 的線性組合，只要確保線性組合的 vector 中最後一項仍然是 $K$，都可以組成合理的 $d$。
5. 當推算出合理的 $d$ 之後就可以找出 flag 了。

> Flag

![](/pic/hw1/11.png)

## \[HW1\] Power Analysis

- Flag: `FLAG{W0ckAwocKaWoCka1}`

### 解題過程 & 思路

1. 依照教授提供的演算法便能解出此題的 flag。
2. 對於 AES 128 每個 byte 來說，需要計算對於所有 key 可能的數值，接著計算 `key^pt`、查表 sbox 做出轉換，然後根據平台性質選擇 hamming weight model 作為 correlation coefficient 計算的依據，最後計算轉換後數值的 hamming weight 與對於所有 power consumption 計算 correlation coefficient，此結果的 `argmax` 便是這個 byte 的 flag。

> Reference

1. [python - Get the position of the largest value in a multi-dimensional NumPy array - Stack Overflow](https://stackoverflow.com/questions/3584243/get-the-position-of-the-largest-value-in-a-multi-dimensional-numpy-array)

> Flag

![](/pic/hw1/12.png)
