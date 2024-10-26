import time

import numpy as np

from midi import check_midi
from utils import reduce_white

def run_slowfade(par_chain, strip_chain, mIn):
    scale = .1
    i = 0
    j = 900
    k = 1800
    t = np.arange(3600) * np.pi / 180. * scale
    signal = np.sin(t)

    print("RUN SLOWFADE")

    while True:

        # if mIn.midiDevice:
        #     if mIn.midiDevice.poll():
        #         events = mIn.midiDevice.read(1)
        #         ev_data = events[0][0]
        #         button = ev_data[1]
        #         ev_value = ev_data[2]

        #         if button == 14:
        #             red_val = ev_value * 2
        #         elif button == 15:
        #             green_val = ev_value * 2
        #         elif button == 16:
        #             blue_val = ev_value * 2
        #         elif button == 17:
        #             white_val = ev_value * 2

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        else:
            red_val = int((signal[i] + 1.) * 127.)
            green_val = int((signal[j] + 1.) * 127.)
            blue_val = int((signal[k] + 1.) * 127.)
            white_val = 0

            red_val, green_val, blue_val = reduce_white(red_val, green_val, blue_val, 1.)
            red_val, green_val, blue_val = reduce_white(red_val, green_val, blue_val, .25)

            i += 1
            j += 2
            k += 3
            if i >= len(t):
                i = 0
            if j >= len(t):
                j = 0
            if k >= len(t):
                k = 0
            par_chain.set_segment(0, par_chain.num_lights, red_val, green_val, blue_val, white_val)
            time.sleep(.05)
