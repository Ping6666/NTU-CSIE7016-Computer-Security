# HW3

## \[Lab\] Stackoverflow

- Flag: `flag{Y0u_know_hoW2L3@k_canAry}`

### 解題過程 & 思路

1. 先 leak 出 canary，再做 buffer overflow，就搞定了。
2. 值得注意的事情是跳過去 return addr 時，stack 需要 align，不然沒辦法通過檢查。

> Reference

1. [movaps XMMWORD PTR [rsp], xmm1 - Google 搜尋](https://www.google.com/search?q=movaps+XMMWORD+PTR+%5Brsp%5D%2C+xmm1)

> Flag

![](/pic/hw3/1.png)

## \[Lab\] Shellcode

- Flag: `flag{How_you_do0o0o0o_sysca1111111}`

### 解題過程 & 思路

1. 寫一個 shellcode，但是需要繞過 0x05, 0x0f 的檢查。
2. 稍微對 syscall 的注入方法有點改動就行。

> Reference

1. [5. C內聯彙編](https://shihyu.github.io/books/ch19s05.html)
2. [What is the function of the push / pop instructions used on registers in x86 assembly? - Stack Overflow](https://stackoverflow.com/questions/4584089/what-is-the-function-of-the-push-pop-instructions-used-on-registers-in-x86-ass)

> Flag

![](/pic/hw3/2.png)

## \[Lab\] Got

- Flag: `flag{Libccccccccccccccccccccccccccc}`

### 解題過程 & 思路

1. 因為輸入沒做範圍檢查，可以對 arr 做範圍外的讀寫，再加上保護只有 Partial RELRO，所以改道 GOT (Global Offset Table) 便能開出 shell。

> Reference

1. [How to find out the dynamic libraries executables loads when run? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/120015/how-to-find-out-the-dynamic-libraries-executables-loads-when-run)
2. [12.04 - strings: '/lib/libc.so.6': No such file - Ask Ubuntu](https://askubuntu.com/questions/189835/strings-lib-libc-so-6-no-such-file)

> Flag

![](/pic/hw3/3.png)

## \[HW3\] Notepad

- Flag Q1: `flag{Sh3l1cod3_but_y0u_c@nnot_get_she!!}`
- Flag Q2: `nan`
- Flag Q3: `nan`

### 解題過程 & 思路

1. 對於第一題: 感謝助教的提示，使用 Path Traversal 搞定，發現需要 `../` 3 次 & notename 需要 padding 至 107 位，才能夠把前面的 subfolder 與 後面 `.txt` 蓋掉，完成後便能夠讀到 `/flag_user`。
2. 對於第二題: 一樣感謝助教的提示，在查資料的過程發現，原來可以透過讀 `/proc/self/maps` 檔案與寫 `/proc/self/mem` 達到控制 process memory content 的效果。所以便嘗試看看能否在 libc 的可執行段塞入 shellcode，藉此與 backend 互動以拿到 flag_backend。下列是嘗試過的方法：
    1. 先測試 shellcode 是否有效果，單純的 write 一些 mem 內容至程式的輸出，也確實能夠得到一些資訊。
    2. 一開始小誤會 flag 所在的位置，想說直接 ORW `/flag_backend`，但後來想想好像不太對，`/flag_backend` 應該是在後端而不是前端。
    3. 中間也有測試過用一些 shellcode 嘗試把 seccomp 關掉，但是嘗試後卻無果。
    4. 最後嘗試的方法都環繞在建立新的 socket & connect to backend，並嘗試塞入 cmd 0x8787，不過經過無數次的嘗試，backend 都沒有如預期的給我 flag。


> Reference

1. [pwnlib.shellcraft.amd64 — Shellcode for AMD64 — pwntools 2.2.1 documentation](https://python3-pwntools.readthedocs.io/en/latest/shellcraft/amd64.html)
2. [CTFtime.org / Real World CTF 4th / QLaaS / Writeup](https://ctftime.org/writeup/32134)
3. [shellcode题目整理 - 跳跳糖](https://tttang.com/archive/1447/)
4. [pwn系列之shellcode（二） - 予柒 - 博客园](https://www.cnblogs.com/xyqer/articles/15553092.html)

> Flag

![](/pic/hw3/4.png)

## \[Lab\] ROP_RW

- Flag: `flag{ShUsHuSHU}`

### 解題過程 & 思路

1. 因為這題是 statically linked，所以幾乎各式各樣的事情都可以做，再加上題目在輸入時沒有做長度檢查， 所以可以透過 buffer overflow 建出 ROP，並通過 check function 的檢查以拿到 flag。

> Flag

![](/pic/hw3/5.png)

## \[Lab\] ROP_Syscall

- Flag: `flag{www.youtube.com/watch?v=apN1VxXKio4}`

### 解題過程 & 思路

1. 與 ROP_RW 幾乎相同概念，只是這題以開出 shell 為目標。

> Flag

![](/pic/hw3/6.png)

## \[Lab\] ret2plt

- Flag: `flag{__libc_csu_init_1s_P0w3RFu1l!!}`

### 解題過程 & 思路

1. 因為這題的保護都沒有開，所以可以透過 rop 一直跳回去 plt，首先 leak 出 put 在 got 上的位置 & 修改它變成 system，之後再執行他並帶入 `/bin/sh` 以開出 shell。

> Flag

![](/pic/hw3/7.png)

## \[Lab\] Stack Pivot

- Flag: `flag{www.youtube.com/watch?v=VLxvVPNpU04}`

### 解題過程 & 思路

1. 這題可以做到 buffer overflow，但是能夠寫的空間稍顯不夠，所以分了三次把 open, read, write 完成，便能夠取得 flag。
2. 值得注意的事情，雖然只需要控制 rdx 的值，不用控制到 rbx 的值，但不確定為什麼只做 pop rdx 會做不出 ORW，一定要弄 pop rdx ; pop rbx 才能夠順利執行。

> Reference

1. [Linux System Call Table for x86 64 · Ryan A. Chapman](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

> Flag

![](/pic/hw3/8.png)

## \[Lab\] FMT

- Flag: `flag{www.youtube.com/watch?v=Ci_zad39Uhw}`

### 解題過程 & 思路

1. 這題可以做到 Format String Attack，所以先 leak 出 main 的 addr.，接者透過 objdump 算出 main 與 flag 之間的 offset，最後再次透過 Format String Attack 印出 flag addr 的值就能夠拿到 flag 了。

> Flag

![](/pic/hw3/9.png)

## \[HW3\] HACHAMA

- Flag: `nan`

### 解題過程 & 思路

1. 這題觀察出一些想法
    1. 因為變數 `msg`, `n2` 的記憶體位置很近，想說如果變數 `name` & `msg` 可以有 buffer overflow，那應該可以修改到 `n2` 的數值。
    2. 如果能修改到 `n2` 的數值，將其改得更大的話，那就可以有更大的 buffer overflow 空間，接者便能夠 leak 出 canary 的數值，在下次 read, write 時應該就可以寫入 rop chain 對 `/home/chal/flag.txt` 做 ORW (Open Read Write)，如此便能夠取得 flag。
2. 發現 msg[0x20] 空間只有 32 格，`read(0, name, 20)` 與 `strcat(msg, " hachamachama")` 合併後最大會到 33 格，正好可以蓋掉 n2 的數值，從 0x30 改變成 0x61 (aka. ”a”)，也就是 strcat 字串的最後一個字元。
3. 但是由於 buf2 占了 0x30，stack 上還有 canary & rbp，所以實際上能夠 ROP 的大小只有 0x18 可以寫。
4. 在這麼小的空間，有嘗試了下列方法:
    1. 透過 one_gadget 找開 shell 的位置，雖然大部分都有符合 constraint，但是執行 `execve` 直接被 seccomp 檢查擋下來。
    2. leak 出 libc 位置，並使用 ROPgadget 在 libc 中找 pop rdi，想要直接做到 `system('/bin/sh')`，但不知為何被 sigemptyset 檢查擋住；後來透過 rt_sigreturn, sigreturn 試圖重設 signal 卻也沒甚麼效果，一樣會得到 Program terminated with signal SIGSEGV, Segmentation fault. 的結果。
    3. 最後也有嘗試 ORW 的方法，嘗試在多次 while loop 中完成 ROP chain，不過沒有成功嘗試出來。

> Reference

1. [gdb - Find the exact address of variable Buf - Stack Overflow](https://stackoverflow.com/questions/4462915/find-the-exact-address-of-variable-buf)
2. [安裝 Ruby](https://www.ruby-lang.org/zh_tw/documentation/installation/)
3. [david942j/one_gadget: The best tool for finding one gadget RCE in libc.so.6](https://github.com/david942j/one_gadget)
4. [x86 calling conventions - Wikipedia](https://en.wikipedia.org/wiki/X86_calling_conventions)
5. [PWN 入門 - rop, gadget 是什麼？](https://tech-blog.cymetrics.io/posts/crystal/pwn-intro-2/)
6. [2020 程安 Pwn 筆記1 - HackMD](https://hackmd.io/@minyeon/r13y1246P)
7. [linux 下起shell失败的分析](https://o0xmuhe.github.io/2016/11/10/linux-%E4%B8%8B%E8%B5%B7shell%E5%A4%B1%E8%B4%A5%E7%9A%84%E5%88%86%E6%9E%90/)
8. [python pwntools库 简介 主要功能有 网络 进程 文件 编解码 elf 汇编 调试-CSDN博客](https://blog.csdn.net/whatday/article/details/128090860)
9. [CS2022 Pwn writeup - HackMD](https://hackmd.io/@Chtsai873/Bkh-uXcPs)

## \[Lab\] UAF

- Flag: `flag{https://www.youtube.com/watch?v=CUSUhXqThjY}`

### 解題過程 & 思路

1. 典型的 UAF 題目，透過申請到與原先 entity 相同的記憶體位置，修改其值變成 `system` & `/bin/sh`，在透過 UAF 達到執行此 event 便能夠開出 shell。
2. 值得注意的是，這題有先給予 gift，拿到了 libc & heap 的位置，所以才能夠順利的建出 payload，以及拿到 flag。(見 `main.py`)
3. 在練習中我有嘗試不靠 gift leak 出 libc 的位置 & heap 的位置。
    1. leak libc 的位置 (見下方 `leak_heap.py`): 需要申請到 unsorted bin 再輸出其內容，便有 libc + 特定 offset 的值。
    2. leak heap 的位置 (見下方 `leak_libc.py`): 只需要申請到 tcache 再輸出其內容，便有 heap 的位置。

> leak_heap.py

```python
context.arch = 'amd64'

uaf_worker = UAFWorker(10057)

uaf_worker.conn.recvuntil(b'gift1: ')
system_addr = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(system_addr) = }")

uaf_worker.conn.recvuntil(b'gift2: ')
heap_leak = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(heap_leak) = }")

uaf_worker.register_entity(0)
uaf_worker.register_entity(1)
uaf_worker.register_entity(2)

uaf_worker.delete_entity(0)
uaf_worker.delete_entity(1)
uaf_worker.set_name(2, 0x18, b'')

print(f"{hex(system_addr) = }")
print(f"{hex(heap_leak) = }")

uaf_worker.interactive()
# 4 2
# will show heap base
```

> laek_libc.py

```python
context.arch = 'amd64'

uaf_worker = UAFWorker(10057)

uaf_worker.conn.recvuntil(b'gift1: ')
system_addr = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(system_addr) = }")

uaf_worker.conn.recvuntil(b'gift2: ')
heap_leak = int(uaf_worker.conn.recvline().strip(), 16)
print(f"{hex(heap_leak) = }")

# need to malloc and free into unsorted bin

for i in range(0x9):
    uaf_worker.register_entity(i)
    uaf_worker.set_name(i, 0x88, b'a')

for i in range(0x9):
    uaf_worker.delete_entity(i)

for i in range(0x8):
    uaf_worker.register_entity(i)
    uaf_worker.set_name(i, 0x88, b'a')

print(f"{hex(system_addr) = }")
print(f"{hex(heap_leak) = }")

uaf_worker.interactive()
# 4 7
# will show libc base
```

> Flag

![](/pic/hw3/10.png)

## \[Lab\] Double Free

- Flag: `nan`

### 解題過程 & 思路

1. 根據助教的提示，這題需要透過修改 __free_hook 變成 system，並透過新申請記憶體時代入 `sh` 字串以取得 shell。
2. 這題首先 leak 出 libc 的位置，以利算出 __free_hook & system 的位置。
3. 接下來要做 Double Free，首先需要填滿 tcache，之後完成 Double Free 的 chain，但是不知為何一直無法通過 `malloc(): unaligned tcache chunk detected` 的檢查。
    1. 試過各式各樣能想到的方法，想辦法給 `aligned` 的記憶體位置或是多塞一些進去 heap，可是都沒有很成功。
4. 所以這題卡關，沒辦法成功 exp。

> Reference

1. [gdb heapinfo - Google 搜尋](https://www.google.com/search?q=gdb+heapinfo)
2. [【CTF资料-0x0002】PWN简易Linux堆利用入门教程by arttnba3_tcache key-CSDN博客](https://blog.csdn.net/arttnba3/article/details/114055329)
3. [PWN cheatsheet - HackMD](https://hackmd.io/@u1f383/pwn-cheatsheet)
4. [資訊安全實務 write up - HackMD](https://hackmd.io/_Pu0GT_vRaywozC9KPgHzg?view#Note)
5. [0CTF: babyheap - Nightmare](https://guyinatuxedo.github.io/28-fastbin_attack/0ctf_babyheap/index.html)
6. [Safe-Linking - Eliminating a 20 year-old malloc() exploit primitive - Check Point Research](https://research.checkpoint.com/2020/safe-linking-eliminating-a-20-year-old-malloc-exploit-primitive/)
7. [Cards - HackMD](https://hackmd.io/@HKraw/Hk32JoaZD)
8. [浅谈glibc新版本保护机制及绕过方法 – 绿盟科技技术博客](https://blog.nsfocus.net/glibc-234/)

## \[HW3\] UAF++

- Flag: `flag{Y0u_Kn0w_H0w_T0_0veR1aP_N4me_aNd_EnT1Ty!!!}`

### 解題過程 & 思路

1. 這題想對 UAF 依樣畫葫蘆，看能不能與在 UAF 練習的方法一樣，只要成功 leak 出 libc & heap 位置，就能夠拿到 flag。
2. 首先有成功透過 unsorted bin leak 出 libc offset，透過計算即可拿到 system 的位置。
3. 但是不論接者如何操作，如何改變指令的排列組合，都沒有辦法 leak 出 heap 位置。
    1. 在地端測試都只能 leak 出前面 11 bytes，差 2 bytes 就到與 heap 同一個 page 了。
    2. 所以想說暫時先在地端用 vmmap 解出來，遠端用爆搜的方法看看能不能解決。先用 vmmap 看出所在的 page 後，再計算出目標 string 的位置，以下圖為例，就是在 0x52000 的 page 上。

![](/pic/hw3/11.png)

![](/pic/hw3/12.png)
        
4. 如果有了 heap 的位置，就可以塞入 call system 時會代入的字串，經過測試會在 0x830 的 offset 上。
5. 接者就可以申請記憶體來達到 UAF，值得注意的是這題在 register_entity 時，會做兩次 malloc，如果要確保 payload 能蓋到 UAF 的目標 entity，一開始申請的兩塊 entity name 需要與 entity 本身大小不同 (不是 0x18 即可)。
6. 經過測試 call system 時代入的字串可以為下列兩種。
    1. `cat ./src/release/share/flag.txt`: 直接讀檔案 `flag.txt`。(遠端須改為 `cat /home/chal/flag.txt`)
    2. `sh`: 開 shell。

![](/pic/hw3/13.png)

![](/pic/hw3/14.png)

7. 在地端成功 pwn 之後 (成功的 exp 請見 `main.py`)，改到遠端測試，沒想到使用原本地端成功的方法，都沒辦法成功 leak heap 的資訊，就連 heap 位置的前面幾個 bytes 都沒辦法成功 leak，後來也嘗試了各式各樣的方法，仍然還是無法 leak 出 heap 的位置。
8. 經過一長段時間的思考，想起來講者說過 libc 裡面也有 `/bin/sh` 的字串，所以就算我不能 leak 出 heap 位置也沒關係，只要 call system 時代入 libc 中的 `/bin/sh` 的字串即可。(先在地端成功的 exp 請見 `main_local.py`)
9. 另外發現我本地的 libc 版本似乎與遠端的不一致，導致 leak 出來的 libc offset 有所差異，所以使用題目提供的 dockerfile 架起環境後，用 gdb 檢查 offset 確實不一樣，改好 offset 後在 docker container 內 run 便成功 pwn 這題，也順利從遠端拿到 flag。(成功的 exp 請見 `main_remote.py`)

> Reference

1. [记fast_bin attack到patch的三种手法 - 先知社区](https://xz.aliyun.com/t/5868)
2. [[原创]Pwn堆利用学习—— Fastbin-Double-Free ——ACTF_2019_message-Pwn-看雪-安全社区|安全招聘|kanxue.com](https://bbs.kanxue.com/thread-263888.htm)
3. [Linux heap exploit - HackMD](https://hackmd.io/@opp556687/BkAm4kiyD)
4. [CTF/BamboofoxCTF2019/pwn/note at master · LJP-TW/CTF](https://github.com/LJP-TW/CTF/tree/master/BamboofoxCTF2019/pwn/note)
5. [Pwntools 用法整理 - HackMD](https://hackmd.io/5GPj9IKCRbCTeaAhw10DLQ?view)

> Flag

![](/pic/hw3/15.png)
