> Table of contents

- [Environment Setup](#environment-setup)
- [Tools](#tools)
- [Online Tools](#online-tools)

# Environment Setup

## VMware

- [VMware Workstation Player](https://www.vmware.com/products/workstation-player.html)

### ISO

- [Windows Enterprise ISO](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise)
- [Ubuntu ISO](https://ubuntu.com/download)

## Conda

- [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/)

# Tools

- Visual Studio Code (VS Code)
- [IDA Free](https://hex-rays.com/ida-free/) / IDA Pro
- [NationalSecurityAgency/ghidra - Github](https://github.com/NationalSecurityAgency/ghidra)
    - [Java Development Kit (JDK)](https://adoptium.net/temurin/releases/?os=linux&arch=x64&package=jdk&version=17)
    - [Ghidra Installation Guide](https://ghidra-sre.org/InstallationGuide.html#Install)
    - some runtime error fixed
        - [GUI icons not rendering correctly on Ubuntu 22.04 #4400](https://github.com/NationalSecurityAgency/ghidra/issues/4400)
            - set `VMARGS=-Dsun.java2d.opengl=true` in the `/support/launch.properties` file under `ghidra_<version>_PUBLIC` folder.
        - [Runtime error on Ubuntu 22.04 - Could not load the Qt platform plugin "xcb" · Issue #5974 · biolab/orange3](https://github.com/biolab/orange3/issues/5974)
            - run `sudo apt install libxcb-xinerama0`
- [Wireshark](https://www.wireshark.org/download.html)
- [Download Burp Suite Community Edition - PortSwigger](https://portswigger.net/burp/communitydownload)
- [radareorg/radare2 - Github](https://github.com/radareorg/radare2/releases)
- [PyLingual Python Decompiler](https://pylingual.io/)

## Linux Tools

- gdb
    - for installation and setup plz see files under `/env`
    - [longld/peda - Github](https://github.com/longld/peda)
    - [scwuaptx/Pwngdb - Github](https://github.com/scwuaptx/Pwngdb)
    - [gefhugsy/gef - Github](https://github.com/hugsy/gef)
    - [pwndbg/pwndbg - Github](https://github.com/pwndbg/pwndbg)
- binutils
- checksec
- ldd
- readelf
- objdump
- ROPgadget
- one_gadget
- strings
- binwalk

## Windows Tools

- [x64dbg/x64dbg - Github](https://github.com/x64dbg/x64dbg)
    - [x64dbg/ScyllaHide - Github](https://github.com/x64dbg/ScyllaHide/releases)
- [hasherezade/pe-bear - Github](https://github.com/hasherezade/pe-bear)
- [Resource Hacker](https://www.angusj.com/resourcehacker/)

# Online Tools

- [Linux System Call Table for x86 64 · Ryan A. Chapman](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

* [Online - Reverse Shell Generator](https://www.revshells.com/)

- [Decompiler Explorer](https://dogbolt.org/)
- [Compiler Explorer](https://godbolt.org/)

* [Online x86 and x64 Intel Instruction Assembler](https://defuse.ca/online-x86-assembler.htm)
* [Online Assembler and Disassembler](https://shell-storm.org/online/Online-Assembler-and-Disassembler/)

- [ASCII Converter - Hex, decimal, binary, base64, and ASCII converter](https://www.branah.com/ascii-converter)
- [CyberChef](https://gchq.github.io/CyberChef/)

* [Decrypt MD5, SHA1, MySQL, NTLM, SHA256, MD5 Email, SHA256 Email, SHA512, Wordpress, Bcrypt hashes for free online](https://hashes.com/en/decrypt/hash)
* [CrackStation - Online Password Hash Cracking - MD5, SHA1, Linux, Rainbow Tables, etc.](https://crackstation.net/)

- [Try It Online](https://tio.run/#)
    - [TryItOnline - Github](https://github.com/TryItOnline)
- [grep.app | code search](https://grep.app/)

* [CSP Evaluator](https://csp-evaluator.withgoogle.com/)
* [PHP Packagist](https://packagist.org/)
