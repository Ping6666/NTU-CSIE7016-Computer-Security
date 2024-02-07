# peda + pwngdb
define peda

    source ~/peda/peda.py
    source ~/Pwngdb/pwngdb.py
    source ~/Pwngdb/angelheap/gdbinit.py

    define hook-run

        python

import angelheap
angelheap.init_angelheap()

        end

    end

end

# gef
define gef

    source ~/gef/gdbinit-gef.py

end

# pwndbg
define pwndbg

    source ~/pwndbg/gdbinit.py

end
