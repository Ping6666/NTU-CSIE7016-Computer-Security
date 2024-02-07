# AIS3 EOF CTF 2024

- [Hahamut](./%231%20Hahamut/README.md)
- [RUSH P0PP3R](./%232%20RUSH%20P0PP3R/README.md)
- [Instruction Chain Programming Contest](./%233%20Instruction%20Chain%20Programming%20Contest/README.md)
- [Casino](./%234%20Casino/README.md)
- [Pwn2Own](./%235%20Pwn2Own/README.md)

## 簡介

- 可以使用 Internet
- Infra
    - 透過 vpn 連至 jump box 才能碰到題目機
    - 5 分鐘一個回合
        - 部分服務會重製
        - 每回合根據下列等分項來計算分數
            - service check
            - attack
            - defence
            - king
        - 各項分數會先做 norm 再總和成各隊的總分
- Attack and Defense (A/D)
    - Attack
        - attack manager
        - 取得 Flag (Hahamut) / 賺錢 (Casino)
    - Defense
        - 可以透過上傳 patch binary 來對服務做修改 & 防禦
            - 所有隊伍的 patch 會在下一個 round 公布
        - 各隊可以看到自己服務的流量/封包 (pcap)
            - 但會 delay 幾個 round 才公布
- King of the Hill (KoH)
    - 排名賽
    - 每個子題目會有一個 King
    - 每回合重新排名
- Pwn2Own
    - 流程
        - 公布 firmware，各隊可以對其找任意的漏洞並取得權限。
        - 如果有隊伍成功 demo，則會修正 firmware 並再次公布，往後則無法透過相同漏洞得分。
        - 以此流程反覆，直到所有回合結束。
    - own?
        - 以此次競賽為例，需使得 Raspberry Pi display target video。

## Write-up

[writeup](./writeup.md)
