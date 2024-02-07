# RUSH P0PP3R

> KoH

Rush Rush Rush! Let's be a POP chain finder! http://10.102.100.30/

## Rules

TL;DR: 找到網路上隨便一個 composer package 裡的反序列化 RCE gadget，越好用+越短越好。

- 你可以安裝任意一個存在的 composer package，目標是找到一個能執行任意 function 的反序列化 gadget
- 你需要使用 p0pp3r_win function 來執行 ./@ --give-me-flag 指令
- 只有 p0pp3r_win 是有效的目標，其他任何的 function 都不會被計分系統接受，就算其能成功達成 RCE
- 你的 payload 中必須至少使用到一個直接屬於 package 的 namespace 裡的 class（根據 psr-0、psr-4 判斷）
- 對於每一個 package，只會存在一個最佳 gadget 能獲得分數，比較順位如下：
  - Gadget 依賴條件：毋需條件 > __toString > __call
  - Payload 長度：短的可以取代長的
  - Package 星星數越多，其價值分數越高
- 分數計算以執行完成的時刻為準，而非提交時間；若一個 payload 尚未執行完畢，無法嘗試第二個
- 一律安裝「2024/2/3 10:00 UTC+8 前」釋出的最新一個版本
- 執行環境為 docker 映像 php:cli，原始碼大致上如下：

```
<?php
require 'vendor/autoload.php';
function p0pp3r_win($command) {
  system($command);
}
unserialize(PAYLOAD);
```

```
<?php unserialize(base64_decode(PAYLOAD));
<?php echo unserialize(base64_decode(PAYLOAD));
<?php unserialize(base64_decode(PAYLOAD))->r4nd0m_m3th0d();
```
