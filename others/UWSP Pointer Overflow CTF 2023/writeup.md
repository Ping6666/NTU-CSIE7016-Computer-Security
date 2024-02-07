# Pointer Overflow CTF 2023

## CTF 資訊 & 結果

- [CTFtime.org / Pointer Overflow CTF - 2023](https://ctftime.org/event/2026/)
- Date: September 17th, 2023 to January 21st, 2024
- Rating weight: 0
- 隊伍名稱: ^poctf{.*}$
- 名次: 47/1910
- 總得分: 3400

![](/pic/poctf/1.png)

![](/pic/poctf/2.png)

## Unquestioned and Unrestrained

- Crypto, 100 points, 944 solved.
- Flag: `poctf{uwsp_411_y0u2_8453_423_8310n9_70_u5}`

### 解題過程 & 思路

1. 此題是入門題，使用 base64 decoder 即可解開。

## A Pale, Violet Light

- Crypto, 200 points, 437 solved.
- Flag: `poctf{uwsp_533k 4nd y3 5h411 f1nd}`

### 解題過程 & 思路

1. 題目提供 RSA 的結果、公鑰，但由於 $N$ 過小，使得可以得出原先的兩個質數，如此便能得出密鑰並解出 Flag。

> Reference

1. [RSA加密演算法 - 維基百科，自由的百科全書](https://zh.wikipedia.org/zh-tw/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95)

## Missing and Missed

- Crypto, 300 points, 745 solved.
- Flag: `poctf{uwsp_219h7_w20n9_02_f0290773n}`

### 解題過程 & 思路

1. 題目提供的字串由 ><+-.,[] 所組成的，查了資料才知道這是 brain fuck，使用 online solver 解出 Flag。

> Reference

1. [Brainfuck - 維基百科，自由的百科全書](https://zh.wikipedia.org/zh-tw/Brainfuck)
2. [Online Brainfuck Compiler](https://www.tutorialspoint.com/execute_brainfk_online.php)
3. [Brainfuck Visualizer](https://ashupk.github.io/Brainfuck/brainfuck-visualizer-master/index.html)

## Here You See A Passer By

- Misc, 200 points, 603 solved.
- Flag: `poctf{uwsp_pr377y_bu7_p377y_bu7_pr377y}`

### 解題過程 & 思路

1. 題目提供一個 pdf，以迷宮為圖像，只要能解出迷宮，就能得到 Flag。

> Flag

![](/pic/poctf/3.png)

## If You Don't, Remember Me

- Forensics, 100 points, 389 solved.
- Flag: `poctf{uwsp_w31c0m3_70_7h3_94m3}`

### 解題過程 & 思路

1. 題目提供一個 pdf 檔案，用文字編輯器能發現存在有 flag 相同格式的內容，`poctf(uwsp_77333163306D335F37305F3768335F39346D33}`，更進一步觀察，內容是由 16 進位 ascii 所組成，完成轉換後便能得出 Flag。

> Reference

1. [ASCII Converter - Hex, decimal, binary, base64, and ASCII converter](https://www.branah.com/ascii-converter)

## A Petty Wage in Regret

- Forensics, 200 points, 263 solved.
- Flag: `poctf{uwsp_7h3_w0rld_h4d_17_f1257}`

### 解題過程 & 思路

1. 此題題目提供一張照片，另於其他題目中曾經提供過一些工具，結合使用便能得出全部的 Flag。
2. 於照片的文字段解出前半部分的 Flag，`::P1/2:: poctf{uwsp_7h3_w0rld_h4d`。
3. 並使用線上工具對圖片做操作，便能夠得出後半部分的 Flag，`::P2/2:: 17_f1257`。

> Reference

1. [NVSTGT - Welcome to Flavortown.](https://nvstgt.com/)
2. [Forensically, free online photo forensics tools - 29a.ch](https://29a.ch/photo-forensics/#forensic-magnifier)
3. [ASCII Converter - Hex, decimal, binary, base64, and ASCII converter](https://www.branah.com/ascii-converter)

> Flag

![](/pic/poctf/4.png)

![](/pic/poctf/5.png)

## The Gentle Rocking of the Sun

- Crack, 200 points, 346 solved.
- Flag: `poctf{uwsp_c411f02n14_d234m1n9}`

### 解題過程 & 思路

1. 題目提供 “crack2 = 4bd939ed2e01ed1e8540ed137763d73cd8590323” 字串與一個加密過後的檔案，想了很久+查了許多資料，發現原來是可能是 Hash 過後的結果。
2. 使用線上工具還原出 hash 前的內容為 `zwischen`，以此解開加密檔案，便能夠發現 Flag 是以層層的資料夾名稱所組成的。
    
![](/pic/poctf/6.png)
    

> Reference

1. [Decrypt MD5, SHA1, MySQL, NTLM, SHA256, MD5 Email, SHA256 Email, SHA512, Wordpress, Bcrypt hashes for free online](https://hashes.com/en/decrypt/hash)
2. [CrackStation - Online Password Hash Cracking - MD5, SHA1, Linux, Rainbow Tables, etc.](https://crackstation.net/)

## Easy as it Gets

- Reversing, 100 points, 309 solved.
- Flag: `poctf{uwsp_4d_v1c70r14m_w4573l4nd3r}`

### 解題過程 & 思路

1. 題目提供一個 powershell script，沒想到沒把註解內密碼移除，使用註解的內容，再用線上跑 script 的工具即可得出 Flag。

> Reference

1. [PowerShell – Try It Online](https://tio.run/#powershell)

> Flag

![](/pic/poctf/7.png)

## A Tangled Web We Weave

- Reversing, 200 points, 261 solved.
- Flag: `poctf{uwsp_k1n9_k0n9_907_n07h1n9_0n_m3}`

### 解題過程 & 思路

1. 題目提供一個 asm，有初始數值 & 演算法，但是把過程中 xor 的數值去除了，所以簡單的實作出一致的演算法然後爆搜 xor 的內容，就能夠得出 Flag 了。

> Reference

1. [x86 - What does "int 0x80" mean in assembly code? - Stack Overflow](https://stackoverflow.com/questions/1817577/what-does-int-0x80-mean-in-assembly-code)
2. [咕咕鐘扮鬼臉: 在 Linux 下寫組語, 透過 int 0x80 使用 system call](https://guguclock.blogspot.com/2009/01/linux-int-0x80-system-call.html)

## Sunshine on Filth is Not Polluted

- Reversing, 300 points, 77 solved.
- Flag: `poctf{uwsp_7h3_1355_y0u_kn0w_7h3_837732}`

### 解題過程 & 思路

1. 題目提供兩個 hash 過後的提示，分別是下列兩者。
    1. `f704f57ea420275ad51bf55b7dec2c96` md5 Uninitialized
    2. `87cd8b8808600624d8c590cfc2e6e94b` md5 variables
2. 使用 ida 觀察題目的流程。
    
![](/pic/poctf/8.png)

![](/pic/poctf/9.png)

![](/pic/poctf/10.png)

![](/pic/poctf/11.png)
    
3. 程式碼流程為隨機產生 admin 的 auth_code，但是在輸入使用者名稱時，沒有檢查輸出與輸入的順序，另外透過 ida 觀察到 src & v1 在 stack 上佔有相同的位置，所以可以先 leak 出 v1 (aka. auth_code) 的內容。
4. 如此輸入 admin 與 leak 出的內容便能拿到 shell，便能得到 Flag。

> Flag

![](/pic/poctf/12.png)

## A Great Interior Desert

- OSINT, 200 points, 204 solved.
- Flag: `poctf{uwsp_7h3_2357_15_45h}`

### 解題過程 & 思路

1. 這題分類是 OSINT，並提供了一個關鍵字 @free_jack_marigold。
2. 首先可以找到 [https://mastodon.social/@free_jack_marigold](https://mastodon.social/@free_jack_marigold)，在其中找到另一個提示 @jock_bronson。
    
![](/pic/poctf/13.png)
    
3. 接者可以找到 [https://twitter.com/jock_bronson](https://twitter.com/jock_bronson)，在其的追蹤名單可以看到另一個帳號。
    
![](/pic/poctf/14.png)

![](/pic/poctf/15.png)

4. 再次依樣畫葫蘆，在追蹤名單中帳號的追蹤名單。可以發現神奇連結指向另一個 IG 帳號，[https://www.instagram.com/senorspacecakes/](https://www.instagram.com/senorspacecakes/)。
    
![](/pic/poctf/16.png)

![](/pic/poctf/17.png)

5. 能夠看到在此 IG 帳號帳號便有含有 Flag 的圖片。
    
![](/pic/poctf/18.png)

![](/pic/poctf/19.png)


## We Rest Upon a Single Hope

- Web, 100 points, 588 solved.
- Flag: `poctf{uwsp_1_4m_4ll_7h47_7h3r3_15_0f_7h3_m057_r34l}`

### 解題過程 & 思路

1. 這題是一個網頁會檢查使用者的輸入，前端檢查輸入 key 是否等於 v，通過檢查便會在 console 吐出 Flag；所以就透過 dev tools 拿出 v 的數值，並作為 key submit，就順利拿到 Flag 了。
    
![](/pic/poctf/20.png)

![](/pic/poctf/21.png)


## Vigil of the Ceaseless Eyes

- Web, 200 points, 318 solved.
- Flag: `poctf{uwsp_71m3_15_4n_1llu510n}`

### 解題過程 & 思路

1. 題目雖然是一個留言板網頁，不過有提示 flag 存在路徑 `/secret/flag.pdf` 之中。
    
![](/pic/poctf/22.png)
    
2. 後來想想用 curl 工具讀此檔案，便成功拿到 Flag 了。
    
![](/pic/poctf/23.png)
    

## Quantity is Not Abundance

- Web, 300 points, 141 solved.
- Flag: `poctf{uwsp_1_h4v3_70_1n5157}`

### 解題過程 & 思路

1. 這題是一個圈圈叉叉的網頁，題目有提示 Flag 在路徑 `/.secret/flag.txt` 底下，但是需要權限。
    
![](/pic/poctf/24.png)
    
2. 這題還有額外提示需要修改網頁中的 function，之後就是開始通靈 & 瘋狂測試。
3. 可以解出來完全是誤打誤撞，修改 tie 之後會 call 到的程式碼，去訪問 flag，然後遊玩兩場一模一樣的遊戲，就可以拿到 Flag 了。
    
![](/pic/poctf/25.png)

![](/pic/poctf/26.png)
    

## Absence Makes Hearts Go Yonder

- Stego, 100 points, 488 solved.
- Flag: `poctf{uwsp_h342d_y0u_7h3_f1257_71m3}`

### 解題過程 & 思路

1. 題目提供 gif 檔案作為附件，用文字編輯器打開就看到 Flag 啦。

## My Friend, A Loathsome Worm

- Exploit, 100 points, 139 solved.
- Flag: `poctf{uwsp_5w337_c10v32_4nd_50f7_511k}`

### 解題過程 & 思路

1. 首先先用 ida 看看程式邏輯，發現會檢查 v6 的數值，比對正確才會給 shell。有觀察到可以做輸入並且會存在 v4 之中，因為都在 stack 上且輸入沒有做長度檢查，所以可以蓋到 v6 如此就可以取得 shell。
    
![](/pic/poctf/27.png)
    
2. 用 gdb 驗證想法，並找出要覆蓋的長度。
    
![](/pic/poctf/39.png)

![](/pic/poctf/40.png)
    
3. 填入正確數字就有 shell，就能夠取得 Flag 了。
    
![](/pic/poctf/28.png)
    

## A Guilded Lily

- Exploit, 200 points, 58 solved.
- Flag: `poctf{uwsp_4_57udy_1n_5c42137}`

### 解題過程 & 思路

1. 題目有給提示是與 BOF (Buffer Overflow) 有關，另外有給關鍵字 Heartbleed bug。
2. 一樣先用 ida 看程式邏輯，發現輸入沒做長度檢查，所以可以做 ROP chain。但是發現保護全開，所以需要先 leak 出資訊才可以做 BOF。
    
![](/pic/poctf/29.png)

![](/pic/poctf/30.png)
    
3. 首先先 leak 出 canary，之後再 BOF 塞入 ROP  chain，填入 `/bin/sh` 字串 & call syscall。
    
![](/pic/poctf/31.png)
    

> Reference

1. [心臟出血漏洞 - 維基百科，自由的百科全書](https://zh.wikipedia.org/zh-tw/%E5%BF%83%E8%84%8F%E5%87%BA%E8%A1%80%E6%BC%8F%E6%B4%9E)
2. [Stack Buffer Overflow - HackMD](https://hackmd.io/@pLhjJSzGRy-wZAgbtvHFJw/HkRbLy8GF)
3. [NCU ADL CTF(Project 1) 2022 Writeups - Alan’s Blog](https://lebr0nli.github.io/blog/security/NCU-ADL-2022/)

## Time is but a Window

- Exploit, 300 points, 97 solved.
- Flag: `poctf{uwsp_71m3_15_4_f4c702}`

### 解題過程 & 思路

1. 先用 ida 觀察題目流程，發現流程為 main → greet → get_string，而 get_string 的地方能做 BOF。

![](/pic/poctf/32.png)

![](/pic/poctf/33.png)

![](/pic/poctf/34.png)
    
2. 另外還觀察到這題給了一個開 shell 的 function。
    
![](/pic/poctf/35.png)
    
3. 發現這題檢查開得很神祕，沒有 canary 可以順利 BOF 沒錯，但是 PIE 卻打開了，需要思考怎麼計算正確的 return address 到 win function。
    
![](/pic/poctf/36.png)
    
4. 觀察了許久，最後用 objdump 時看到原先 get_string 的 return function greet 與 win function 沒有差太遠，所以在做 BOF 時只需要蓋到 return addr. last 8 bits，好在是 little endian。
    
![](/pic/poctf/37.png)
    
5. 搞定 BOF 就有 shell，也就能拿到 Flag。

![](/pic/poctf/38.png)
