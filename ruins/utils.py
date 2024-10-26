import time

import numpy as np

def reduce_white(r, g, b, amt):
    val = np.min((r, g, b)) * amt
    r -= val
    g -= val
    b -= val

    return int(r), int(g), int(b)

def reduce_blue(r, g, b, amt):
    val = b * amt
    r += val // 2
    if (r > 255): r = 255
    g += val // 2
    if (g > 255): g = 255
    b -= val

    return int(r), int(g), int(b)

def calculate_color(m1, m2, i, num_sends):
    return (m1 - (m1 - m2) * 1. * i / num_sends).astype(int)

def fade_colors(par_chain, strip_chain, m1, m2, num_sends, send_rate, brightness_factor=3):
    par_pick = np.random.randint(0,4)

    for i in range(num_sends):
        # calculate color
        c = calculate_color(m1, m2, i, num_sends)
        c = c // brightness_factor

        # send color
        par_chain.set_segment(0, par_chain.num_lights, c[:,0], c[:,1], c[:,2], c[:,3])

        strip_chain.set_segment(0, strip_chain.num_lights, c[par_pick,0], c[par_pick,1], c[par_pick,2], 0)

        # wait
        time.sleep(send_rate)

def _create_shuffled_eye(ndim):
    shuffled_eye = np.eye(ndim)
    np.random.shuffle(shuffled_eye)
    return shuffled_eye

def create_shuffled_eye(ndim, shuffle_white=False):
    if shuffle_white:
        shuffled_eye = _create_shuffled_eye(ndim)
    else:
        shuffled_eye = _create_shuffled_eye(ndim - 1)
        eye = np.eye(ndim)
        eye[:ndim - 1, :ndim - 1] = shuffled_eye
        return eye

def make_array(color, num, pre=np.empty(0), post=np.empty(0)):
    return np.concatenate((pre, np.array([color] * num), post))

def random_color(max_val=255):
    return int(np.random.random() * max_val)

def random_rgbw(max_val=255, white=False, reduce_w=False):
    white_val = random_color(max_val) if white else 0
    rgb_color = (
        random_color(max_val), # r
        random_color(max_val), # g
        random_color(max_val), # b
    )
    if reduce_w:
        rgb_color = reduce_white(*rgb_color, 1)
    return np.array([
            *rgb_color,
            white_val # w
        ])

chosen_rgbs = [
    (255,164,0), # bright orange
    (254,80,0), # construction orange
    (255,133,15), # turmeric
    (255,153,19), # goldfish orange
    (220,88,42), # dark orange
    (161,0,14), # rich red
    (122, 33, 16), # pacific blue complimentary rust red
    (199, 45, 16), # pacific blue complimentary orange red
    (134,38,51), # maroon
    (255,188,217), # cotton candy pink
    (18, 173, 179), # bright orange complimentary teal
    (32, 18, 179), # bright orange complimentary dark blue
    (5,169,199), # pacific blue
    (21,96,189), # denim blue
    (197,180,227), # light purple
    (153,186,221), # carolina blue
    (0,174,239), # comic book blue
    (198,161,207), # lilac
    (207,87,138), # mulberry
]

def pick_rgbw(max_val=255, white=False, reduce_w=False):
    global chosen_rgbs

    white_val = random_color(max_val) if white else 0
    rgb_index = np.random.randint(0, len(chosen_rgbs))
    rgb_color = chosen_rgbs[rgb_index]
    if reduce_w:
        rgb_color = reduce_white(*rgb_color, 1)
    return np.array([
            *rgb_color,
            white_val # w
        ])
