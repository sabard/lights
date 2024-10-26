import time

import numpy as np

from midi import check_midi
from utils import *

def run_separate(par_chain, strip_chain, mIn, num_seconds=12, send_rate=.2):

    print("RUN SEPARATE")

    num_sends = int(1.0 * num_seconds / send_rate)
    num_colors = 4 # rgbw

    num_pars = par_chain.num_lights
    shuffled_eye = create_shuffled_eye(num_pars)

    first = True
    m_rgb2 = None

    while True:

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        # pick color
        # start_c = random_rgbw(reduce_w=True)
        start_c = pick_rgbw(reduce_w=False)
        print(start_c)
        m_start_c = shuffled_eye.dot(np.tile(start_c, num_pars).reshape(num_colors, num_pars))
        print(m_start_c)
        # TODO check for mismatched colors/pars
        m_rgb1 = m_start_c * shuffled_eye

        if not first:
            # fade from last rgb2 to start color
            print("rgb2 to start color")
            fade_colors(par_chain, strip_chain, m_rgb2, m_start_c, num_sends, send_rate)
        else:
            first = False

        # more accurate time
        # for num_seconds seconds
        # end_time = time.time() + num_seconds
        # while (time.time() < end_time):

        # best effort time
        # fade from start color to rgb1
        print("start color to rgb1")
        fade_colors(par_chain, strip_chain, m_start_c, m_rgb1, num_sends, send_rate)

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        shuffled_eye = create_shuffled_eye(num_pars)

        # end_c = random_rgbw(reduce_w=True)
        end_c = pick_rgbw(reduce_w=False)
        print(end_c)
        m_end_c =  shuffled_eye.dot(np.tile(end_c, num_pars).reshape(num_colors, num_pars))
        m_rgb2 = m_end_c * shuffled_eye

        # fade from rgb1 to rgb2
        print("rgb1 to rgb2")
        fade_colors(par_chain, strip_chain, m_rgb1, m_rgb2, num_sends, send_rate)

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        # fade from rgb2 to end color
        print("rgb2 to end color")
        fade_colors(par_chain, strip_chain, m_rgb2, m_end_c, num_sends, send_rate)

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        # fade from end color to rgb2
        print("end color to rgb2")
        fade_colors(par_chain, strip_chain, m_end_c, m_rgb2, num_sends, send_rate)

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset
