import sys

import angr
import claripy

# import logging

# ref
# https://hackmd.io/@cwXgzjB3S1eEs_BPxM1n8A/ByT-_BuWc

# logging.getLogger('angr.sim_manager').setLevel(logging.DEBUG)

filename = '../src/dist/super_angry'
proj = angr.Project(filename)

# __int64: 8 bytes
argv = claripy.BVS('argv', 8 * 32)

state = proj.factory.entry_state(args=[proj.filename, argv])
simgr = proj.factory.simulation_manager(state)


def _found(s: angr.sim_state.SimState):
    _out = s.posix.dumps(sys.stdout.fileno())
    return b'Correct!' in _out


simgr.explore(find=_found)

if len(simgr.found) > 0:
    print(simgr.found[0].solver.eval(argv, cast_to=bytes))
else:
    print("Fail to solve")
