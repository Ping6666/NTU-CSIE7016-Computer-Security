# AIS3 EOF Qual 2024

![](/pic/ais3_qual/1.png)

![](/pic/ais3_qual/18.png)
![](/pic/ais3_qual/19.png)

# Solved

## Misc - Welcome

- Flag: `AIS3{W3lc0mE_T0_A1S5s_EOF_2o24}`

### 解題過程 & 思路

1. 加入 Discord 的 Flag。

## Reverse - Flag Generator

- Flag: `AIS3{U$1ng_W1nd0wS_I$_sUCh_a_P@1N....}`

### 解題過程 & 思路

1. 這題發現原檔內涵神祕資訊 (有 MZ、PE) 並寫檔，但其實不會幫忙寫檔。

![](/pic/ais3_qual/2.png)

![](/pic/ais3_qual/3.png)
    
2. 所以透過 x64dbg，把目標位置 & 目標內容拿出來，並重新存檔。
    
![](/pic/ais3_qual/13.png)
    
3. 直接執行就看到 Flag 了。
    
![](/pic/ais3_qual/14.png)
    

## Web - DNS Lookup Tool: Final

- Flag: `AIS3{jU$T_3aSy_c0MMAnD_Inj3c7ION}`

### 解題過程 & 思路

1. 這題是簡單的 injection，可是我解了好久，首先發現要繞開的字符有點多，再來發現結果不會顯示出來。
    
![](/pic/ais3_qual/4.png)
    
2. 所以很輕易地能聯想到要使用 webhook，經過測試發現遠端沒有 `wget`，所以只能用 `curl` 來操作。
3. 之後做了許多嘗試發現 `curl` get 的方法沒辦法傳送完整的 `ls` 結果，原本想說可能要用 paste, tr, sed, echo 等等工具的特性，可是都沒辦法收到完整的內容；最後改用 curl post 就搞定了。
    
![](/pic/ais3_qual/15.png)

![](/pic/ais3_qual/16.png)
    

> Reference

1. [Command Injection - HackTricks](https://book.hacktricks.xyz/pentesting-web/command-injection)
2. [OS Command Injection Vulnerability- A beginner’s guide | by Dark-0 | Medium](https://dark-0.medium.com/os-command-injection-vulnerability-a-beginners-guide-811828372be1)
3. [Hacker's Guide](https://yolospacehacker.com/hackersguide/?cat=cmdinjection)
4. [Bypass Bash Restrictions - HackTricks - Boitatech](https://hacktricks.boitatech.com.br/linux-unix/useful-linux-commands/bypass-bash-restrictions)
5. [What is the Difference Between ${} and $() in Bash – TecAdmin](https://tecadmin.net/difference-between-parameter-expansion-and-command-substitution-in-bash/)
6. [Linux tr Command with Examples](https://phoenixnap.com/kb/linux-tr)
7. [hacktricks/linux-hardening/useful-linux-commands/bypass-bash-restrictions.md at master · carlospolop/hacktricks](https://github.com/carlospolop/hacktricks/blob/master/linux-hardening/useful-linux-commands/bypass-bash-restrictions.md)
8. [Linux "ls" Command with Examples](https://www.atatus.com/blog/ls-command-in-linux-with-example/)
9. [How can I replace each newline (\n) with a space using sed? - Stack Overflow](https://stackoverflow.com/questions/1251999/how-can-i-replace-each-newline-n-with-a-space-using-sed)

## Web - Internal

- Flag: `AIS3{jU$T_s0M3_fuNny_N9inX_FEatuRe}`

### 解題過程 & 思路

1. 這題是要繞過 nginx internal 的限制。
    
![](/pic/ais3_qual/5.png)
    
2. 看了 nginx spec 發現在做 redirect 時會帶上 “X-Accel-Redirect” 的 header，查了資料發現可以使用 CRLF 的漏洞達到 CRLF Injection 自定義的 header，如此便能夠繞過 nginx internal 的限制。
    
![](/pic/ais3_qual/17.png)
    

> Reference

1. [urllib.parse — Parse URLs into components — Python 3.12.1 documentation](https://docs.python.org/3/library/urllib.parse.html)
2. [Module ngx_http_core_module](https://nginx.org/en/docs/http/ngx_http_core_module.html#internal)
3. [X-Accel | NGINX](https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/)
4. [CVE-2021-29084: Exploiting CRLF Header Injection in Synology NAS for Unauthenticated File Downloads – Justin Taft](https://justintaft.com/blog/cve-2021-29084-synology-crlf-unauthenticated-file-downloads)
5. [Midnight Sun CTF 2019 Quals](https://balsn.tw/ctf_writeup/20190406-midnightsunctf/)

## Reverse - Stateful

- Flag: `AIS3{@re_Y0u_@_sTAtEful_0r_STateLeS$_CtfeR}`

### 解題過程 & 思路

1. 這題先看看流程，發現是輸入長度為 43 的字串，並經過 state machine 後需要經過字串的比較，如果通過則表示原本輸入的就是 Flag。
    
![](/pic/ais3_qual/6.png)
    
2. 接者發現 state machine 是由一個 while loop 內含著一連串的 if else (switch case) 所組成 (太長了就不附圖)，原本想用 angr 解，但是不太會用，所以只好用時間堆出這題的解法。
3. 首先先解出 state 的運算順序 (見 state.py)；接者由最後比較的 hex list (圖中的 k_target)，逆著操作回去原本的輸入字串，最後解出 `wIS3{@re_Y0u_@_sTAtEful_0r_STateLeS$_CtfeR}`，合理推測是我 state 其中的部分寫錯，將解出的資訊改成 Flag 正確的格式 (第一個 w 改成 A)，就能答對了。
    
![](/pic/ais3_qual/7.png)
    

# Unsolved (學習紀錄)

## Crypto - Baby Side Channel Attack

- 這題賽後才解出來
- Flag: `AIS3{S1de_ChaNn3L_1$_3@$y_wh3n_THe_DAtA_l34k4G3_1S_3xaCT}`

### 解題過程 & 思路

1. 這題因為運算的過程都在 trace 內，所以 $e, d$ 很輕易的就能得知。
    
![](/pic/ais3_qual/8.png)
    
2. 所以只需要能夠有兩個數是 $n$ 的倍數，就可以用 gcd 算出 $n$，如此便能算出 $m$，也就能拿到 flag。
3. 可是我的數學太差了，所以一直在 $phi$ & $n$ 的倍數中打轉；賽後看出題者在 Discord 的分享，才發現我寫錯的地方，真的是殘念。
    
![](/pic/ais3_qual/9.png)
    

## Pwn - jackpot

- Flag: 沒解出來

### 解題過程 & 思路

1. 這題輸入 name 的部分開太大了，有 BOF 的漏洞，另外 ticket_pool 存取沒有檢查邊界，所以可以 leak 出 libc 的資訊。
    
![](/pic/ais3_qual/10.png)
    
2. 原本以為 remote 的 jackpot 裡面真的會吐給我 flag，沒想到 flag 字串沒有修改，還是 fake。
3. 所以只能自己完成 ROP chain，不知為何這個程式本身幾乎沒有 ROP 可以利用，也沒有內含 syscall；不過好險 ticket_pool 可以 leak 出 libc 資訊，所以尋找對應版本 libc 的 ROP chain & syscall。
4. 不過奇怪的事情是，我可以透過 ROP chain 嘗試執行 `system('/bin/sh')`，remote 也會如預期的吐出 Bad system call，代表確實被 seccomp 擋住。
5. 但是我想透過 ROP chain 做 ORW 讀取在跟目錄的 flag 時，卻無法成功；在地端反覆測試也會卡在 ROP chain 之中的 syscall。不太確定是為何，所以這題沒能成功得到 Flag。

> Reference

1. [Online Assembler and Disassembler](https://shell-storm.org/online/Online-Assembler-and-Disassembler/)
2. [Online x86 and x64 Intel Instruction Assembler](https://defuse.ca/online-x86-assembler.htm)
3. [[pwn]ROP：灵活运用syscall_pwn syscall-CSDN博客](https://blog.csdn.net/Breeze_CAT/article/details/100087036)

## Reverse - PixelClicker

- Flag: 沒解出來

### 解題過程 & 思路

1. 這題會給一個 600 * 600 的 bitmap。
    
![](/pic/ais3_qual/11.png)
    
2. 如果依照順序點完全部的 bit，則可以通過檢查，應該就會吐出 Flag；不過題目提示有說可以只點兩下滑鼠就有 Flag，但是不知為何我沒有找到相關的程式邏輯。
    
![](/pic/ais3_qual/12.png)
    
3. 所以合理推測  Flag 應該藏在程式碼內，但是跑起來看、或是透過 radare2 在 rsrc 裡面找都找不到 QQ。

> Reference

1. [NTU 惡意軟體逆向實驗室 2 撰寫 - HackMD](https://hackmd.io/@SBK6401/SJJjgR1Uj)

## Web - copypasta

- Flag: 沒解出來

### 解題過程 & 思路

1. 這題很有趣，會根據使用者給的內容，填入模板之中。
2. 賽後看 Discord 內的分享原來是可以透過 python format string 的方法達到 injection。

## Web - HTML Debugger

- Flag: 沒解出來

### 解題過程 & 思路

1. 這題要繞過 `DOMPurify.sanitize` & `encodeURIComponent`。
2. 參考了下列的 ref 能夠成功繞過 DOMPurify 的限制，可是繞過 encodeURIComponent 的部分卻沒嘗試出來。

> Reference

1. [Live DOM Viewer](https://software.hixie.ch/utilities/js/live-dom-viewer/)
2. [Bypassing DOMPurify again with mutation XSS | PortSwigger Research](https://portswigger.net/research/bypassing-dompurify-again-with-mutation-xss)
3. [Mutation XSS via namespace confusion - DOMPurify < 2.0.17 bypass - research.securitum.com](https://research.securitum.com/mutation-xss-via-mathml-mutation-dompurify-2-0-17-bypass/)
4. [Writeup - Sanity (AmateursCTF 2023) - Justin Applegate](https://justinapplegate.me/2023/amactf-sanity/)

## Crypto - Baby AES

- Flag: 沒解出來

### 解題過程 & 思路

1. 這題可以在任意大小的 block 任意的使用 CFB, OFB, CTR 做加密。
2. 我猜可以使用 CTR 洩漏出之後 iv 的資訊 or CTR 的 same iv attack；不過只有大概的猜想，沒有實際想出應該如何利用。

> Reference

1. [Block cipher mode of operation - Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Common_modes)
2. [Crypto日记之AES-CTR Stream Cipher Reuse Attack_crypto aes ctr-CSDN博客](https://blog.csdn.net/zgzhzywzd/article/details/123507172)

# Scoreboard

![](/pic/ais3_qual/20.png)
