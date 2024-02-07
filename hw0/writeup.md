# CS HW0

## \[HW0\] Easy C2

### 解題觀察 & 思路

1. 使用 ghidra 觀察程式邏輯，並且反組譯能夠發現下列行為。
2. 連線至 `127.0.0.1:11187` 、decode flag 並傳送 flag。(如下圖)

![](/pic/hw0/1.png)

### 解題過程 & 方法

1. 在相應的 port 建立 server。
2. 跑程式，就可以收到 flag 了。

> Reference

1. [bash - How to wait for an open port with netcat? - Stack Overflow](https://stackoverflow.com/questions/27599839/how-to-wait-for-an-open-port-with-netcat)
2. [shell - Forward SIGTERM to child in Bash - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/146756/forward-sigterm-to-child-in-bash)

### Flag

`FLAG{C2_cmd_in_http_header}`

![](/pic/hw0/2.png)

## \[HW0\] GUSP Hub

### 解題觀察 & 思路

1. 此題需要我們完成 GUSP 服務，能夠完成符合 `app.js` 檢查的服務，便能夠取得 api id。
2. 接者是 xss 的部分，bot 拿到 flag 後要怎麼回傳給我，想了好久才想到 web 最基本的功能 fetch，搞定後 flag 就能夠拿到手了。

### 解題過程 & 方法

1. 架設符合 `app.js` 檢查規範的服務。
2. 設定 Cookies，前往 [http://edu-ctf.zoolab.org:10010/add-api](http://edu-ctf.zoolab.org:10010/add-api) 上傳 url (服務 ip 位置) & javascript (請 bot 幫忙執行的 xss)，便能取得 api id。
3. 前往 [http://edu-ctf.zoolab.org:10010/report](http://edu-ctf.zoolab.org:10010/report) 上傳 api id & alias (route on the flask)，便能在 server 收到 bot 幫忙看的 flag。

![](/pic/hw0/3.png)

> Reference

1. [python - Flask: get current route - Stack Overflow](https://stackoverflow.com/questions/21498694/flask-get-current-route)

### Flag

`FLAG{web progr4mming 101}`

![](/pic/hw0/4.png)

## \[HW0\] Baby Crackme

### 解題觀察 & 思路

1. 使用線上工具 [Decompiler Explorer](https://dogbolt.org/) 的 Hex-Rays (aka. IDA)，觀察到下圖行為。
2. 如果可以復刻相同邏輯，便可以繞過 license 的檢查，直接算出 flag。

![](/pic/hw0/5.png)

### 解題過程 & 方法

1. 用 ghidra 找出目標陣列 (byte_2020) 的數值。
2. 用 C 復刻相同邏輯，即可以算出 flag。

### Flag

`FLAG{r0ll1ng_4nd_3xtr4ct_t0_m3m0ry}`

![](/pic/hw0/6.png)

## \[HW0\] Baby Hook

### 解題觀察 & 思路

1. 此題用到 `LD_PRELOAD` 的功能，可以替換掉或是在 runtime 填上 shared libraries，如此可以覆蓋掉原先 shared libraries function 的功能。
2. 因此只需要編譯一個 shared object，其具有目標 function 相同的名稱 & input & ouput 數量、type，並上傳便能取得 flag。

### 解題過程 & 方法

1. 寫隻 C 並編譯成 shared object。
2. 使用工具上傳 & 接收 response (也就是 flag)。

> Reference

1. [LD_PRELOAD的偷梁换柱之能 - Net66 - 博客园](https://www.cnblogs.com/net66/p/5609026.html)
2. [In C, how should I read a text file and print all strings - Stack Overflow](https://stackoverflow.com/questions/3463426/in-c-how-should-i-read-a-text-file-and-print-all-strings)

### Flag

`b'\n296803\nFLAG{B4by_Ld_Pr3L0aD_L1bR1rY_:)}You win!! Maybe :)\n'`

![](/pic/hw0/7.png)

## \[HW0\] Extreme Xorrrrr

### 解題觀察 & 思路

1. 此題會先找出質數，接者做質數運算，再跑 xor 運算。
2. 首先發現 xor 運算的 function，具有性質 $f(f(x))=x$。
3. 接者透過模反元素，可以使得 mod 前的數值還原，只留下 secret。
4. 另外因為 mod 運算皆為質數，所以可以使用 “中國剩餘定理 (Chinese Remainder Theorem, CRT)” 計算並推回原本的 flag，因此上網找如何解 crt & mod mul inv。(也可以使用 SageMath)

### 解題過程 & 方法

1. 計算 xor，還原原本的 hint, muls, mods。
2. 透過模反元素算出解 CRT 所需必要的資訊。
3. 計算 CRT 就得出最小可能的 flag 了，此也正好是此題的 flag。

> Reference

1. [algorithm - Modular multiplicative inverse function in Python - Stack Overflow](https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)
2. [Chinese Remainder Theorem Using Python | by Anjan Parajuli | Analytics Vidhya | Medium](https://medium.com/analytics-vidhya/chinese-remainder-theorem-using-python-25f051e391fc)

### Flag

`b'FLAG{xor_ThEN_><OR_1qUal_ZEr0}'`

![](/pic/hw0/8.png)
