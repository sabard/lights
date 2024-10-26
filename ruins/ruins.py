from lights import DmxChain
from midi import MidiKeyboard
from utils import *

from manual import run_manual
from slowfade import run_slowfade
from separate import run_separate
from swirl import run_swirl
from spookems import run_spookems

# # local
# STRIP_IP = "127.0.0.1"
# STRIP_PORT = 21324

# PAR_IP = "127.0.0.1"
# PAR_PORT = 21325
# PYGAME_MIDI_DEVICE = None

# studio
# STRIP_IP = "172.17.3.41"
# STRIP_PORT = 21324

# PAR_IP = "172.17.3.43"
# PAR_PORT = 21324

# prod
STRIP_IP = "192.168.88.21"
STRIP_PORT = 21324

PAR_IP = "192.168.88.20"
PAR_PORT = 21324
PYGAME_MIDI_DEVICE=0


TIMEOUT = 2

NUM_PARS = 4
NUM_STRIPS = 16

mIn = MidiKeyboard()

par_chain = DmxChain(NUM_PARS, PAR_IP, PAR_PORT)
strip_chain = DmxChain(NUM_STRIPS, STRIP_IP, STRIP_PORT)

presets = [
    run_spookems,
    run_manual,
    run_slowfade,
    run_separate,
    run_swirl,
]

preset_idx = 0
def run_next(to_next=None):
    global preset_idx, par_chain, strip_chain, mIn

    if to_next is None:
        pass
    elif to_next:
        preset_idx += 1
        if preset_idx == len(presets):
            preset_idx = 0
    else:
        preset_idx -= 1
        if preset_idx < 0:
            preset_idx = len(presets) -1

    return presets[preset_idx](par_chain, strip_chain, mIn)


to_next = None
while True:
    to_next = run_next(to_next)

