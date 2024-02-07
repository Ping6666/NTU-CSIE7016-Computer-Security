# HW2

## \[Lab\] AssemblyDev

- Flag: `FLAG{c0d1Ng_1n_a5s3mB1y_i5_sO_fun!}`

### 解題過程 & 思路

1. 依照題目要求完成 `asm` 就搞定了。

> Reference

1. [assembly - x64 asm: Moving a negative value from a register to memory - Stack Overflow](https://stackoverflow.com/questions/64482357/x64-asm-moving-a-negative-value-from-a-register-to-memory)
2. [x86 - MUL function in assembly - Stack Overflow](https://stackoverflow.com/questions/40893026/mul-function-in-assembly)
3. [c - Accessing the low 32-bits of r8 through r15 - Stack Overflow](https://stackoverflow.com/questions/48861606/accessing-the-low-32-bits-of-r8-through-r15)
4. [if statement - How to write if-else in assembly? - Stack Overflow](https://stackoverflow.com/questions/40602029/how-to-write-if-else-in-assembly)
5. [binary - How to compare a signed value and an unsigned value in x86 assembly - Stack Overflow](https://stackoverflow.com/questions/27284895/how-to-compare-a-signed-value-and-an-unsigned-value-in-x86-assembly)
6. [Intel x86 JUMP quick reference](http://unixwiz.net/techtips/x86-jumps.html)
7. [x86 - assembly check if number is even - Stack Overflow](https://stackoverflow.com/questions/49116747/assembly-check-if-number-is-even)
8. [MUL — Unsigned Multiply](https://www.felixcloutier.com/x86/mul.html)
9. [DIV — Unsigned Divide](https://www.felixcloutier.com/x86/div.html)

> Flag

![](/pic/hw2/1.png)

## \[Lab\] HelloRevWorld

- Flag: `FLAG{h311O_revers1ng_3ngineer5}`

### 解題過程 & 思路

1. 程式跑起來就有 flag。

> Flag

![](/pic/hw2/2.png)

## \[HW2\] crackme_vectorization

- RevGuard Session: `fgp5FdHX/7z2E1BCJxvPD5crfc1JyGC8DUY7XKjoU+vl3vE=`
- Flag: `FLAG{yOu_kn0w_hOw_to_r3v3r53_4_m47riX!}`

### 解題過程 & 思路

1. 這題使用 ida 先做靜態分析，能夠發現一直出現 lucky number 7 & `sqrt`，可以合理推測有 49 個 input numbers，經過中間的 `vector_1300` 運算後，再與 `.rodata` 中 `unk_20E0` 的值比較，如果比較正確，則說明找到正確的 Session。
    
![](/pic/hw2/3.png)
    
2. 在 `vector_1300` 中前半部分先做了輸入資訊有效性的檢查 (lucky number 7)，中間則是做了一堆 vector 運算，透過運算的結果會影響到輸出的內容。這邊做了一些假設，有些正確有些錯誤。
    1. `_ECX` 不會受到 input numbers 影響。(錯誤)
    2. 對於存入結果運算的 index 在計算 for-loop 過程中不會重複。(錯誤)
    3. input numbers index 與 src index 在做 `*` 運算時，具有 1-1 對應的關係。(正確)
    4. 觀察到在取 input numbers index 時，有對 index 做 `* magic` 運算，推測具有二維對應的關係 (二維矩陣)。(正確)
        
![](/pic/hw2/4.png)
        
3. 由於 vector 運算的 asm 過於複雜，所以利用 gdb 對程式做動態分析。(詳細可見 payload.py)
    1. 為了抓出 `main` 邏輯中 `memcmp` 的對象，首先需要找到正確的 `malloc` 位置，利用 gdb break 於 `malloc`，並在 `malloc` return 時取出 `rax` 的值，這也就是 `malloc` 新的空間的記憶體位置。
    2. 取得位置後，便可以使用 payload 測試 input numbers，將 payload 以 49 個 0 表示，首先測試 `payload[0] = 1` 與 `payload[0] = 2`，發現 input 與 output 存在線性關係，也發現 `mask` 的存在，接著測試 `payload[1~6] = 1`，驗證了上述說法；最後測試 `payload[7] = 1`，得知取 mask 前後對 input numbers & `_ECX` 的影響，如此順利完成最後的拼圖。 (分析過程的內容請參見資料夾內的 `payload_result.txt` 檔案)
4. 有了上述的邏輯 (加上一些運氣不錯的通靈)，便可以將問題改變成矩陣運算，$`Ax = y`$，其中 input numbers 就是所求的 $x$，`s2`  就是已知的 $y$，而 `src` 還有使用 gdb 找出的 `mask` 能構成已知的 $A$。
    1. 有了數學限制式子，便能夠過 sagemath 工具解出未知數 $x$。
5. 有了 $x$，便找出 session，便能與 server 交換得到 flag。

> RevGuard Session

![](/pic/hw2/5.png)

> Flag

![](/pic/hw2/60.png)

## \[Lab\] Clipboard Stealer

- Flag Q1: `FLAG{T1547.001}`
- Flag Q2: `FLAG{T1480}`
- Flag Q3: `FLAG{th15_I4_4_mut3x_k1LL_SwitcH}`
- Flag Q4: `FLAG{462fe0007f86957f59824e113f78947c}`
- Flag Q5: `FLAG{C2_cU540m_Pr0t0C01}`
- Flag Q6: `FLAG{MessageBoxA}`

### 解題過程 & 思路

1. 感謝助教一步一步教學。
2. 首先第一題 (sub_140001C80) 知道方法是 file copy to startup menu folder，去 attack mitre 尋找便能找到 [Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder, Sub-technique T1547.001 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1547/001/)。
    
![](/pic/hw2/6.png)
    
3. 而第二題 (sub_140001030) 知道方法是 execute if meet constraint，去 attack mitre 尋找便能找到 [Execution Guardrails, Technique T1480 - Enterprise | MITRE ATT&CK®](https://attack.mitre.org/techniques/T1480/)。
    
![](/pic/hw2/7.png)
    
4. 對於第三題 (sub_140001120) 只需要依樣畫葫蘆便能解出 flag。
    
![](/pic/hw2/8.png)

![](/pic/hw2/9.png)
    
5. 接者第四題 (Extract Next Stage Payload)，找到程式 PE 的存放位置，將目標位置的資料改成 array 並匯出。計算匯出檔案的 md5 hash: `certutil -hashfile ./export_next_stage.dll md5`。
    
![](/pic/hw2/10.png)
    
![](/pic/hw2/11.png)
    
![](/pic/hw2/12.png)
    
6. 接者第五題 (Exfiltrate Data)，觀察 `next_stage.dll` 程式邏輯。
    1. 發現 debug info 被留下來了。
    2. 在 `connect_to_c2` 中發現 c2 與 `0xA0AA8C0` 的 `11187u` 做溝通，也就是 `192.168.10.10:11187`。
    3. 觀察 `send_collected_data_to_c2` 流程與透過 Wireshark 觀察附上的 `capture.pcapng` 檔案。能夠發現加密演算法是 RC4，key 是 `f0 c7 d3 0e 7f 2c 15 ba`，enc data 則是 `43 60 5b 5f 4e ba 9f 9e e3 78 6f 55 cb 81 24 fa e7 bf 0d 1b 3c 24 b7 4e`。使用線上工具 [RC4 - CyberChef](https://gchq.github.io/CyberChef/#recipe=RC4(%7B'option':'Hex','string':''%7D,'Hex','Latin1')) 還原出原本的明文。

![](/pic/hw2/13.png)

![](/pic/hw2/14.png)

![](/pic/hw2/15.png)

![](/pic/hw2/16.png)

7. 最後第六題 (Dynamic API Resolution)，觀察 `my_start` 中尋找 `user32.dll` function 的判斷與計算，復刻出一樣的邏輯與判斷就可以取得 flag。
    
![](/pic/hw2/17.png)


> Reference

1. [Hex-Rays v7.4 Decompiler Comparison Page – Hex Rays](https://hex-rays.com/products/decompiler/compare/v74_vs_v73/)
2. [c++ - Resolving RVA's for Import and Export tables within a PE file - Stack Overflow](https://stackoverflow.com/questions/2975639/resolving-rvas-for-import-and-export-tables-within-a-pe-file)

## \[HW2\] Banana Donut Verifier

- RevGuard Session: `zls4wq/r/wzzU5gE1yAxN5crfc1JyGC8DUY7XKjoU+vl3vE=`
- Flag: `FLAG{d0_Y0u_l1k3_b4n4Na_d0Nut?}`

### 解題過程 & 思路

1. 這題先用 ida 跑靜態分析，首先發現程式會先 `scanf` 一段字串，接者發現在畫 donut 的過程會對輸入的字串做操作，最後會對輸入字串與 `off_6050` (aka. `.rodata` 中 `byte_2010`) 的值比較。
    1. 雖然 “畫 donut 的過程” 看似簡單，有機會可以逆向出 `x_idx` & `y_idx` 的數值，但是發現對輸入字串做的操作更加的簡單。此操作不但 index 不重複且操作都是 xor。
    2. 此外 ida 有好心幫我算出 `scanf` 存入的地址與 `rsp` & `rbp` 的 offset (如圖中的 `v21`)。
    3. 如此一來可以使用上面程式的邏輯，再加上 stack frame 在進出 function 前後長的 layout 會一致的特性，便可以用動態分析的方法搞定。

![](/pic/hw2/18.png)

![](/pic/hw2/19.png)

2. 接者使用 gdb 對程式做動態分析。(詳細可見 payload.py)
    1. 首先需要塞入 padload (以 `b’1’ * 1024` 為例子)，並撈出於 stack frame 的位置，並驗證進出 function 前後 stack frame layout 是一致的。
    2. 在利用 `rbp` & `rsp` 的數值關係驗證此事後，使用 gdb break 在 `usleep` 的位置，因為在此之後輸入字串 & `off_6050` 的值應該要一致，後面的檢查才能通過。
    3. 再者由於輸入字串會被操作的方法只有 xor，所以只需要 leak 出在此階段，輸入字串於 stack frame 的內容與 `off_6050` 的內容，就可以取得正確的輸入了。
3. 實作出上述方法，藉由輸入字串已知，操作後的輸入字串也是已知，`off_6050` 的內容也是已知；如此一來變成功取得正確輸入，便找出 session，便能與 server 交換得到 flag。

> Reference

1. [c++ - Mistake using scanf - Stack Overflow](https://stackoverflow.com/questions/10227281/mistake-using-scanf)
2. [c - Input non-printable ascii characters into scanf - Stack Overflow](https://stackoverflow.com/questions/41683969/input-non-printable-ascii-characters-into-scanf)
3. [1091 電腦攻擊與防禦 GDB_&_pwntools.pdf — BY TA 瓈 方](https://staff.csie.ncu.edu.tw/hsufh/COURSES/SPRING2022/GDB_&_pwntools.pdf)
4. [c++ - How to use GDB to find what function a memory address corresponds to - Stack Overflow](https://stackoverflow.com/questions/7639309/how-to-use-gdb-to-find-what-function-a-memory-address-corresponds-to)
5. [macos - How to use malloc in asm - Stack Overflow](https://stackoverflow.com/questions/59697603/how-to-use-malloc-in-asm)

> RevGuard Session

![](/pic/hw2/20.png)

> Flag

![](/pic/hw2/59.png)

## \[Lab\] Super Angry

- Flag: `FLAG{knowing_how_2_angr!}`

### 解題過程 & 思路

1. 使用 ida 觀察程式邏輯，能發現藉由控制 `argv` 能達到控制程式 if-else 邏輯。
2. 因此使用工具 angr 解出此題。
    
![](/pic/hw2/21.png)
    

> Reference

1. [angr - HackMD](https://hackmd.io/@cwXgzjB3S1eEs_BPxM1n8A/ByT-_BuWc)
2. [day1-r1-a-1.pdf Binary 自動分析的那些事 - YSc](https://hitcon.org/2016/CMT/slide/day1-r1-a-1.pdf)
3. [hacktricks/reversing/reversing-tools-basic-methods/angr/angr-examples.md at master · carlospolop/hacktricks](https://github.com/carlospolop/hacktricks/blob/master/reversing/reversing-tools-basic-methods/angr/angr-examples.md)
4. [Angr CTF从入门到入门（2）_angr_ctf怎么编译jinja文件-CSDN博客](https://blog.csdn.net/u013648063/article/details/108831809)
5. [Angr入门（二）- 一些CTF的Angr分析-CSDN博客](https://blog.csdn.net/qq_44370676/article/details/119741664)
6. [angr-doc/examples/9447_nobranch/solve.py at master · angr/angr-doc](https://github.com/angr/angr-doc/blob/master/examples/9447_nobranch/solve.py)

> Flag

![](/pic/hw2/22.png)

## \[Lab\] Scramble

- Flag: `FLAG{scramble_and_using_solver_to_solve_it}`

### 解題過程 & 思路

1. 使用 z3，給定 constrain 並解出 flag。

> Flag

![](/pic/hw2/23.png)

## \[Lab\] Unpackme

- Flag: `FLAG{just_4_simple_unpackme_challenge!}`

### 解題過程 & 思路

1. 此題直接使用 UPX 會遇到一些問題，但是其實不靠 UPX，此個 unpackme 程式仍可以順利執行，所以使用其他解決方法。
    1. 感謝助教提示，原來可以用 patch 的方法繞過 checksum，不過我已經用其他方法先搞定此題了。

![](/pic/hw2/24.png)

2. 由於程式能正常執行，換言之 runtime 時 upx 可以正常解開程式邏輯，所以採取其他方法，強制送給程式 SIGSEGV (signal segmentation violation)，這樣 OS 便會幫忙 core dump。如此就能拿到 runtime upx 解開的 elf，如此也就能好好逆向了。(流程請見下方 SIGSEGV)
3. 將 elf 交給 ida，可以看出程式邏輯非常的簡單，用 python 複刻出一致的邏輯便能夠求出 flag。
    
![](/pic/hw2/25.png)
    

> SIGSEGV

```bash
# os version
$ uname -r
6.2.0-36-generic
$ cat /etc/os-release
Ubuntu 22.04.2 LTS

# set the maximum size of core files created
$ ulimit -c unlimited

# run the proc and send signal
$ ./src/dist/unpackme &
$ ps
$ kill -11 $PID
$ bg

# copy the core dumped file
$ cp /var/lib/apport/coredump/$core_dumped_filename .
$ file $core_dumped_filename
ELF 64-bit LSB core file, x86-64, version 1 (SYSV), SVR4-style, from './src/dist/unpackme',
real uid: 1000, effective uid: 1000, real gid: 1000, effective gid: 1000,
execfn: './src/dist/unpackme', platform: 'x86_64'
```

> Reference

1. [員外 Security: Defcon 17 Wargame 競賽解題心得](https://timhsu.chroot.org/2009/06/defcon17wargame.html)
2. [c - Core dumped, but core file is not in the current directory? - Stack Overflow](https://stackoverflow.com/questions/2065912/core-dumped-but-core-file-is-not-in-the-current-directory)

> Flag

![](/pic/hw2/26.png)

## \[HW2\] Baby Ransom

- Flag Q1: `FLAG{e6b77096375bcff4c8bc765e599fbbc0}`
- Flag Q2: `FLAG{50_y0u_p4y_7h3_r4n50m?!hmmmmm}`

### 解題過程 & 思路

1. 先說說在用 ida 靜態分析過程中發現的趣事，一開始以為 ida 給的 entry point 其中一個一定會是程式的 main function，沒想到其實這個 main 雖然包含了平常寫程式的 entry point，還有額外 PE 會先做的事情，如: `_InterlockedCompareExchange`, `initterm`, `TlsCallback`, `VirtualProtect`。這些有的是為了多執行緒 (synchronization, global/static objects, data)、有的是為了 env, argv 的設定、有的則是為了 memory permission 的設定。結果在逆向時看了許多這類跟環境相關卻與實際邏輯無關的 function…。
    1. 雖然 Clipboard Stealer 有這些內容，但因為這題一開始是助教一步一步帶著完成的，所以當初沒有發現，後來重做時才發現這些酷酷的東西。
2. 首先在 `main_1DBB` 中可以發現程式會先一個網站是否存在，不存在才會繼續執行。(好像跟 WannaCry 滿類似的?!)
    
![](/pic/hw2/27.png)
    
3. 接者在 `url_sub_1B0A` 中，會嘗試移動檔案，但是應該會移動失敗；走入 `caller_3_197A` 一路 call 到 `checkDebugger_and_CreateProc_18DA`，會先檢查 debugger 是否存在，不存在則繼續走入 `createProcess_1653`。
    
![](/pic/hw2/28.png)
    
![](/pic/hw2/29.png)
    
4. 在 `createProcess_1653` 中也就是此隻程式的核心，首先先撈出 resource 也就是第一題 (Next Stage Payload)，之後創建 proc 讓 payload 跑起來。
    
![](/pic/hw2/30.png)
    
5. 在 `get_Resource_68_ptr_size_155A` 中可以看到，要找到名為 68 的 resource，原本要使用 Resource Hacker 把內容撈出來，可是發生一些錯誤，後來改使用 Radare2 才順利撈出，其中地址與大小皆能夠透過 Radare2 `iR` 看到。
    
![](/pic/hw2/31.png)
    
![](/pic/hw2/32.png)
    
6. 原本以為拿錯東西了，不過發現 1187 出現異常的多次，再仔細看看 `get_Resource_68_ptr_size_155A` 發現 resource 68 存的內容需要經過 xor 才可以還原出正確的 PE (或參見 main_q1.py)，還原撈出的檔案後一樣使用 `certutil -hashfile ./payload md5` 便可以求出 flag。
    
![](/pic/hw2/33.png)
    
7. 接者靜態分析還原出來的 Next Stage Payload，在 `show_window_and_inject_1160` 中發現除了 show window 之外會 call function `inject_2870`。
    
![](/pic/hw2/34.png)
    
8. 而在 `inject_2870` 主要會做兩件事情：
    1. 在 `get_fn_from_dll_1B10` 中會先 load library & get function from dll file。
    2. 在 `sub_140001660` 中會檢查連線、下載檔案 & 複製檔案到 Microsoft Update Backup 資料夾 & 加密檔案。
    
![](/pic/hw2/35.png)
    
9. 在 `get_fn_from_dll_1B10` 中會分別從 kernel32.dll, msvcrt.dll, user32.dll, wininet.dll 中找出一些 functions (下圖僅以 msvcrt 為例子)，找出方法是透過 `get_fn_magic_2810` 的結果來篩選。所以先複刻相同檢查並找出載入的 functions 是哪一些，再對程式做更進一步的分析，或參見 functions.py。
    
![](/pic/hw2/36.png)
    
![](/pic/hw2/37.png)
    
10. 在 `sub_140001660` 中，會先透過 `internet_check_28B0` 檢查連線並下載檔案，之後在 `do_rc4_enc_1960` 中則會加密檔案。值得注意的事情是，這邊有找出 SystemFunction033 的函式握把，這是會做 RC4 加密演算法的 function。
    
![](/pic/hw2/38.png)
    
11. 首先是 `internet_check_28B0` 的部分，先下載 [shouldhavecat.com/robots.txt](http://shouldhavecat.com/robots.txt) 並讀取 index 2687~2706 存入 `qword_140007460`。
    
![](/pic/hw2/39.png)
    
12. 在 `do_rc4_enc_1960` 中，可以發現使用了先前找到的 SystemFunction033 的函式握把，`_data` 也就是加密前的內文，`_key` 則是剛剛存入 `qword_140007460` 的內容，另一個值得注意的是 key 會受到目前被加密的檔案名稱影響，以 enc_flag.txt 為例子，原本的檔名是 flag.txt 其長度為 8，所以 key 則只取前 8 位來做 RC4 加密演算法的 key。
    
![](/pic/hw2/40.png)
    
13. 有了上述的逆向結果，可以將第二題 (Encrypted File) 解答，或參見 main_q2.py。

> Reference

1. [Flare-On 7 — 08 Aardvark - explained.re](https://explained.re/posts/flare-on7-aardvark/)
2. [Encrypting Shellcode using SystemFunction032/033 | 🔐Blog of Osanda](https://osandamalith.com/2022/11/10/encrypting-shellcode-using-systemfunction032-033/)
3. [InMemory Shellcode Encryption and Decryption using SystemFunction033 - Intruder](https://www.redteam.cafe/red-team/shellcode-injection/inmemory-shellcode-encryption-and-decryption-using-systemfunction033)
4. [Memory Encryption/Decryption with SystemFunction033 | by S12 - H4CK | Oct, 2023 | Medium](https://medium.com/@s12deff/memory-encryption-decryption-with-systemfunction033-2c391bc2bd89)

> Flag

![](/pic/hw2/41.png)

## \[HW2\] Evil FlagChecker

- Flag: `FLAG{jmp1ng_a1l_ar0und}`

### 解題過程 & 思路

1. 首先先用 ida 做靜態分析，發現在 `main_1450` 一開始會先做 sleep，然後 call 一個神祕的 function `loc_401AE0`，這個 function ida 竟然解不開。
    
![](/pic/hw2/42.png)
    
![](/pic/hw2/43.png)
    
2. 所以先把 `sleep` 帶入的長度改成 0，並且把相關的判斷邏輯改成 nop。
    
![](/pic/hw2/61.png)

![](/pic/hw2/62.png)
    
3. 改好後會變成不等待，也不會自動結束。
    
![](/pic/hw2/44.png)
    
4. 接者改用 x32dbg 看看會跳到哪裡，過程中發現會請 `ntdll.dll` 的 `CCC0` & `91B0` 幫忙做跳轉，並且在 user space 的部分會從 1AE0 → 11ED → 13C0。
    
![](/pic/hw2/45.png)

![](/pic/hw2/46.png)

![](/pic/hw2/47.png)
    
5. 其中 `sub_4013C0` 還算簡單，會先讀取輸入、做一些操作 (`sub_4012A0`)、並輸出判斷結果。
    
![](/pic/hw2/48.png)
    
6. 核心部分 `sub_4012A0`，會先對輸入做操作然後與 `unk_403400` 內容比較一致與否。

![](/pic/hw2/49.png)

![](/pic/hw2/50.png)
    
7. 所以只要複刻出 `sub_4012A0` 執行邏輯，就可以還原出 flag。值得注意的事情，magic fn 是輸入轉成輸出，可是已知的內容只有輸出 `unk_403400`，所以需要先將 magic fn 轉換成 inv magic fn，才有辦法還原成輸入，也就是此題的 flag。

> Reference

1. [Online x86 and x64 Intel Instruction Assembler](https://defuse.ca/online-x86-assembler.htm#disassembly2)
2. [python rol, ror operation implement](https://gist.github.com/trietptm/5cd60ed6add5adad6a34098ce255949a)

> Flag

![](/pic/hw2/51.png)

## \[HW2\] Trashcan

- Flag: `FLAG{s1mpl3_tr4S5_caN}`

### 解題過程 & 思路

1. 一開始一樣用 ida 做靜態分析，但是在 `scanf_1BC0` 卡關許久，覺得這個 function 太複雜，ida 解出來的也不太可讀。
    
![](/pic/hw2/52.png)
    
2. 而 `&Trashcan::vftable’` 指到 `sub_1400013B0` ，這個 function 開頭也做了一些複雜的事情，此時完全沒頭緒這隻程式在做甚麼，只知道吃了 input string，然後做了一些奇妙的事情，最後會吐出結果是 accept 還是 reject。
    
![](/pic/hw2/53.png)

![](/pic/hw2/54.png)
    
3. 之後改用 x64dbg 跑跑看，在 `.rdata` 段發現神秘的東西，雖然感覺滿像是 FLAG 的字串，但想了許久還是覺得沒頭沒尾的。
    
![](/pic/hw2/55.png)
    
4. 想說 ida 可能在解時有點問題，所以也用 ghidra 看看，在相同 function `sub_1400013B0` 中發現另一些神秘的東西。不但有 FLAG 字串的 ASCII 還有左右大括號 `{}` 的 ASCII。
    
![](/pic/hw2/56.png)

![](/pic/hw2/57.png)

5. 因此在認真回去看 ida 解出來的結果 (如第二點的圖片)，發現程式邏輯是會判斷長度為 22 的字串，並且內容要與在 `.rdata` 中 `xmmword_140004480` ~ `xmmword_140004510` 一致；準確地來說是 `.rdata` 的內容會被存放到 `v14~v18` & `v21~v25`，此外 `v19`, `v20`, `v26`, `v27` 都有各自的預設值，所以 `v14~v20` & `v21~v27`，形成了兩個 array。
6. 但是拿出資料後發現似乎 FLAG 字串已經被打亂了，`.rdata` 中的內容被放入第一個 array 其值則是 `FA1345LG{sml_SN_caprt}`，經過一番的觀察~~通靈~~，發現第二個 array 竟然是 0~21 而且都不重複，貌似就是 index 而且還是描述著第一個 array 被打亂前的順序。(詳細可見 main.py)
7. 發現這點之後只需要將打亂後的資料還原，便能夠找出 flag 了。

> Reference

1. [Intel® Intrinsics Guide: _mm_load_si128](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html#text=_mm_load_si128&ig_expand=4063)
2. [Intel® Intrinsics Guide: _mm_store_si128](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html#text=_mm_store_si128&ig_expand=6577)

> Flag

![](/pic/hw2/58.png)
