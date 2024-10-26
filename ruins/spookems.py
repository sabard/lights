import time

import asyncio
import numpy as np

from kasa import Discover, SmartPlug

from midi import check_midi
from utils import reduce_white

FLICKER_DURATION = 10 # seconds
SPOOKEM_DURATION = 60 # seconds

SLEEP_TIME = 0.05 # 50ms

SPEED_FACTOR = 3
INTENSITY = 150
RND_VAL = INTENSITY >> 1

PLUG_IPS = ["192.168.88.11", "192.168.88.12"]

async def turn_off(ip_list):
    for ip in ip_list:
        try:
            p = SmartPlug(ip)
            await asyncio.wait_for(p.update(), timeout=0.5)
            await asyncio.wait_for(p.turn_off(), timeout=0.5)
        except asyncio.TimeoutError:
            print('timeout!')

async def turn_on(ip_list):
    for ip in ip_list:
        try:
            p = SmartPlug(ip)
            await asyncio.wait_for(p.update(), timeout=0.5)
            await asyncio.wait_for(p.turn_on(), timeout=0.5)
        except asyncio.TimeoutError:
            print('timeout!')


# lightning_peaks = 100, 250, 300
# lightning_troughs = 80, 120, 240, 260, 280, 400
def get_lightning_val(t, duration):
    speed = 500. / duration
    t *= 1. * speed
    val = 0
    if t < 80:
        val = 0
    elif t >= 90 and t < 100:
        val = 255 * ((t - 90) / 10)
    elif t >= 100 and t < 110:
        val = 255 * ((110-t) / 10)
    elif t >= 240 and t < 250:
        val = 255 * ((t - 240) / 10)
    elif t >= 250 and t < 260:
        val = 255 * ((260-t) / 10)
    elif t >= 280 and t < 300:
        val = 255 * ((t - 280) / 20)
    elif t >= 300 and t < 350:
        val = 255 * ((350-t) / 50)
    else:
        val = 0

    return int(val)


def run_spookems(par_chain, strip_chain, mIn, color=(200, 0, 5, 0)):

    num_pars = par_chain.num_lights

    print("RUN SPOOKEMS")

    start_time = time.time()

    spookem_time = False

    start_color_mat = np.tile(color, (4, 1))
    color_mat = None

    # flicker vars
    cur_intensities = [0] * num_pars
    target_intensities = [0] * num_pars
    fadesteps = [0] * num_pars

    # spookem vars
    signs_on = False
    lightning_idx = None

    while True:

        next_preset = check_midi(mIn)
        if next_preset is not None:
            return next_preset

        # spookems mcgee!
        if spookem_time:
            cur_time = time.time() - spookem_start_time

            # 5s lights out
            if cur_time <= 5:
                color_mat = np.tile((0,0,0,0), (4, 1))

            # lightning effect for 10s
            elif cur_time > 5 and cur_time <= 15:
                # choose lightning params
                if not lightning_idx:
                    lightning_idx = 0
                    lightning_duration = np.random.randint(10,40)
                    chosen_light = np.random.randint(num_pars)


                # do lightning
                intensity = get_lightning_val(lightning_idx, lightning_duration)
                color_mat = np.tile((0,0,0,0), (4, 1))
                color_mat[chosen_light,:] = np.array([1,1,1,1]) * intensity

                # increment
                lightning_idx += 1

                # reset lightning
                if lightning_idx > lightning_duration:
                    lightning_idx = None

            # 2s lights out
            elif cur_time > 15 and cur_time <= 17:
                  color_mat = np.tile((0,0,0,0), (4, 1))

            # flicker signs for 30s
            elif cur_time > 17 and cur_time <= 47:
                # kasa flicker

                flicker_run = np.random.randint(10)

                for _ in range(flicker_run):
                    if signs_on:
                        asyncio.run(turn_off(PLUG_IPS))
                        signs_on = False
                    else:
                        asyncio.run(turn_on(PLUG_IPS))
                        signs_on = True

                should_sleep = np.random.choice([True, False, False, False])
                time.sleep(np.random.randint(10) * .1)

            # 3s lights out
            elif cur_time > 47 and cur_time <= 50:
                color_mat = np.tile((0,0,0,0), (4, 1))

            # 10s all on bright
            elif cur_time > 50 and cur_time <= 60:
                color_mat = np.tile((0,255,0,0), (4, 1))
                # kasa on
                asyncio.run(turn_on(PLUG_IPS))
                signs_on = True

            # spookem time ends! back to candles
            else:
                lightning_idx = None
                start_time = time.time()
                spookem_time = False
                color_mat = np.tile(color, (4, 1))

                asyncio.run(turn_off(PLUG_IPS))
                signs_on = False



        # flickery
        else:
            if time.time() - start_time > FLICKER_DURATION:
                spookem_time = True
                spookem_start_time = time.time()
                color_mat = np.tile((0, 0, 0, 0), (4, 1))


            for i in range(num_pars):
                s = cur_intensities[i] # cur light value
                s_target = target_intensities[i] # target light value
                fadestep = fadesteps[i] # step value

                if (fadestep == 0): # init values
                    s = 128
                    s_target = 130 + np.random.randint(4)
                    fadestep = 1

                new_target = False
                if (s_target > s): # fade up
                    s += fadestep
                    if (s >= s_target):
                        new_target = True
                else:
                    s -= fadestep
                    if (s <= s_target):
                        new_target = True

                if (new_target):
                    s_target = np.random.randint(RND_VAL) + np.random.randint(RND_VAL) # between 0 and RND_VAL*2 -2 = 252
                    if (s_target < (RND_VAL >> 1)):
                        s_target = (RND_VAL >> 1) + np.random.randint(RND_VAL)
                    s_target += (255 - INTENSITY)

                    if (s_target > s):
                        dif = s_target - s
                    else:
                        dif = s - s_target;

                    fadestep = dif >> SPEED_FACTOR
                    if (fadestep == 0):
                        fadestep = 1

                cur_intensities[i] = s
                target_intensities[i] = s_target
                fadesteps[i] = fadestep

            color_mat = np.diag(np.array(cur_intensities) / 256.).dot(start_color_mat).astype(int)

        par_chain.set_segment(0, par_chain.num_lights, color_mat[:,0], color_mat[:,1], color_mat[:,2], color_mat[:,3])

        time.sleep(SLEEP_TIME)
