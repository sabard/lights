import time

import numpy as np
from scipy import signal as sps

from midi import check_midi

def run_swirl(par_chain, strip_chain, mIn, colors=((255, 165, 0, 0),(0, 0, 255, 0))):

    print("RUN SWIRL")

    num_pars = par_chain.num_lights
    step = 0.001

    i = -1
    t = np.linspace(0, 2*np.pi, 100)

    c1_val = 0.01
    c2_val = (num_pars / 2.) + c1_val

    while True:

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        i += 1
        if i >= len(t):
            i = 0
        if i + num_pars <= len(t):
            t_cur = t[i:i+num_pars]
        else:
            t_cur = t[i:] + t[:i+num_pars-len(t)]


        # triang = sps.windows.triang(t_cur)

        m_c1 = np.tile(colors[0], (num_pars, 1))
        m_c2 = np.tile(colors[1], (num_pars, 1))

        c1_i1 = int(np.floor(c1_val))
        c1_i2 = int(np.ceil(c1_val))
        c1_v1 = c1_val - c1_i1
        c1_v2 = c1_i2 - c1_val
        c1_i2 %= num_pars
        c1_diag = np.zeros(num_pars)
        c1_diag[c1_i1] = c1_v1
        c1_diag[c1_i2] = c1_v2
        c1_diag  = np.diag(c1_diag)

        c2_i1 = int(np.floor(c2_val))
        c2_i2 = int(np.ceil(c2_val))
        c2_v1 = c2_val - c2_i1
        c2_v2 = c2_i2 - c2_val
        c2_i2 %= num_pars
        c2_diag = np.zeros(num_pars)
        c2_diag[c2_i1] = c2_v1
        c2_diag[c2_i2] = c2_v2
        c2_diag  = np.diag(c2_diag)

        m = (c1_diag.dot(m_c1) + c2_diag.dot(m_c2)).astype(int)

        par_chain.set_segment(0, num_pars, m[:,0], m[:,1], m[:,2], m[:,3])
        time.sleep(.05)

        c1_val += step
        c2_val += step

        if c1_val >= num_pars:
            c1_val -= num_pars

        if c2_val >= num_pars:
            c2_val -= num_pars
