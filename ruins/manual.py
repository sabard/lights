import time

import numpy as np

def run_manual(par_chain, strip_chain, mIn):

    print("RUN MANUAL")

    c = np.zeros((4,4), dtype=int)

    while True:
        if mIn.midiDevice:
            if mIn.midiDevice.poll():
                events = mIn.midiDevice.read(128)
                ev_data = events[-1][0]
                button = ev_data[1]
                ev_value = ev_data[2]

                print(button, ev_value)

                if button == 14:
                    c[0][0] = ev_value * 2
                elif button == 15:
                    c[0][1] = ev_value * 2
                elif button == 16:
                    c[0][2] = ev_value * 2

                elif button == 17:
                    c[1][0] = ev_value * 2
                elif button == 18:
                    c[1][1] = ev_value * 2
                elif button == 19:
                    c[1][2] = ev_value * 2

                elif button == 20:
                    c[2][0] = ev_value * 2
                elif button == 21:
                    c[2][1] = ev_value * 2
                elif button == 22:
                    c[2][2] = ev_value * 2

                elif button == 3:
                    c[3][0] = ev_value * 2
                elif button == 4:
                    c[3][1] = ev_value * 2
                elif button == 5:
                    c[3][2] = ev_value * 2

                elif button == 67:
                    if ev_value == 127:
                        return True
                elif button == 64:
                    if ev_value == 127:
                        return False



        # print(c)

        par_chain.set_segment(0, par_chain.num_lights, c[:,0], c[:,1], c[:,2], c[:,3])

        time.sleep(.05)
