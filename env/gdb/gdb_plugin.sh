#!/bin/sh

# -- longld/peda -- #
git clone https://github.com/longld/peda.git ~/peda

# -- scwuaptx/Pwngdb -- #
git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb

# -- gefhugsy/gef -- #
mkdir ~/gef
wget -O ~/gef/gdbinit-gef.py -q https://gef.blah.cat/py

# # -- pwndbg/pwndbg -- #
# git clone https://github.com/pwndbg/pwndbg.git ~/pwndbg
# ~/pwndbg/setup.sh
