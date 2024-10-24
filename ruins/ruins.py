import os

from collections.abc import Iterable
import numpy as np
# from pynput import keyboard
import pygame
import pygame.midi
import socket
import time
from scipy import signal as sps

# from .swirl import run_swirl

# # local
# STRIP_IP = "127.0.0.1"
# STRIP_PORT = 21324

# PAR_IP = "127.0.0.1"
# PAR_PORT = 21325
# PYGAME_MIDI_DEVICE = None

# studio
STRIP_IP = "172.17.3.41"
STRIP_PORT = 21324

PAR_IP = "172.17.3.43"
PAR_PORT = 21324

# prod
# STRIP_IP = "192.168.88.21"
# STRIP_PORT = 21324

# PAR_IP = "192.168.88.20"
# PAR_PORT = 21324
PYGAME_MIDI_DEVICE=0


TIMEOUT = 2

NUM_PARS = 4
NUM_STRIP_LEDS = 16

# red_val = 255
# green_val = 255
# blue_val = 255
red_val = 0
green_val = 0
blue_val = 0
white_val = 255

class MidiKeyboard():
    def __init__(self):
        global red_val

        try:
            pygame.init()
            pygame.midi.init()

            if pygame.midi.get_count() < 1:
                print('Midi board not found!\n')
                red_val = 255  # default to red
                self.midiDevice = None
            else:
                device = PYGAME_MIDI_DEVICE if PYGAME_MIDI_DEVICE is not None else pygame.midi.get_default_input_id()
                self.midiDevice = pygame.midi.Input(device, 100)

        except Exception as e:
            print(e)


def set_segment_par(start, end, r, g, b, w, print_packet=False):
    m = []
    m.append(3) # DRGBW
    m.append(TIMEOUT)

    for i in range(start, end):
        # m.append(i)  # Index of pixel to change

         # pixel red value
        if isinstance(r, Iterable):
            m.append(r[i])
        else:
            m.append(r)

        # pixel green value
        if isinstance(g, Iterable):
            m.append(g[i])
        else:
            m.append(g)

        # pixel blue value
        if isinstance(b, Iterable):
            m.append(b[i])
        else:
            m.append(b)

        # pixel white value
        if isinstance(w, Iterable):
            m.append(w[i])
        else:
            m.append(w)

    if print_packet:
        print(m)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (PAR_IP, PAR_PORT))


def set_segment_strip(start, end, r, g, b, w=None, print_packet=False):
    m = []
    m.append(3) # DRGBW
    m.append(TIMEOUT)

    for i in range(start, end):
        # m.append(i)  # Index of pixel to change

         # pixel red value
        if isinstance(r, Iterable):
            m.append(r[i])
        else:
            m.append(r)

        # pixel green value
        if isinstance(g, Iterable):
            m.append(g[i])
        else:
            m.append(g)

        # pixel blue value
        if isinstance(b, Iterable):
            m.append(b[i])
        else:
            m.append(b)

        # pixel white value
        if w is not None:
            if isinstance(b, Iterable):
                m.append(b[i])
            else:
                m.append(b)

        # m.append(w)  # pixel white value

    if print_packet:
        print(m)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (STRIP_IP, STRIP_PORT))



def on_press(key):
    global red_val, green_val, blue_val

    try:
        c = key.char
    except AttributeError:
        return

    start_idx = 0
    end_idx = NUM_PARS - 1
    print("on: ", start_idx, end_idx)
    set_segment_par(start_idx, end_idx, red_val, green_val, blue_val, white_val)


def on_release(key):
    try:
        c = key.char
    except AttributeError:
        return

    start_idx = 0
    end_idx = NUM_PARS - 1
    print("off: ", start_idx, end_idx)
    set_segment_par(start_idx, end_idx, 0, 0, 0, 0)

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



scale = .1
i = 0
j = 900
k = 1800
t = np.arange(3600) * np.pi / 180. * scale
signal = np.sin(t)

mIn = MidiKeyboard()

# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()

class Par:
    def __init__(self, r, g, b, w):
        self.r = r
        self.g = g
        self.b = b
        self.w = w


    def rgb(self):
        return self.r, self.g, self.b, self.w

    def rgbw(self):
        return self.r, self.g, self.b, self.w

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


def calculate_color(m1, m2, i, num_sends):
    return (m1 - (m1 - m2) * 1. * i / num_sends).astype(int)

def fade_colors(m1, m2, num_sends, send_rate, brightness_factor=3):
    par_pick = np.random.randint(0,4)

    for i in range(num_sends):
        # calculate color
        c = calculate_color(m1, m2, i, num_sends)
        c = c // brightness_factor

        # send color
        set_segment_par(0, NUM_PARS, c[:,0], c[:,1], c[:,2], c[:,3])

        set_segment_strip(0, NUM_STRIP_LEDS, c[par_pick,0], c[par_pick,1], c[par_pick,2], 0)

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


def check_midi():
    if mIn.midiDevice:
        if mIn.midiDevice.poll():
            events = mIn.midiDevice.read(1)
            ev_data = events[0][0]
            button = ev_data[1]
            ev_value = ev_data[2]

            print(events)

            if button == 67:
                if ev_value == 127:
                    return True
            elif button == 64:
                if ev_value == 127:
                    return False

    return None


def run_slowfade():
    global i,j,k,signal

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

        next_preset = check_midi()
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
            set_segment_par(0, NUM_PARS, red_val, green_val, blue_val, white_val)
            time.sleep(.05)


def run_separate(num_seconds=12, send_rate=.2):

    print("RUN SEPARATE")

    num_sends = int(1.0 * num_seconds / send_rate)
    num_colors = 4 # rgbw

    shuffled_eye = create_shuffled_eye(NUM_PARS)

    first = True
    m_rgb2 = None

    while True:

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset

        # pick color
        # start_c = random_rgbw(reduce_w=True)
        start_c = pick_rgbw(reduce_w=False)
        print(start_c)
        m_start_c = shuffled_eye.dot(np.tile(start_c, NUM_PARS).reshape(num_colors, NUM_PARS))
        print(m_start_c)
        # TODO check for mismatched colors/pars
        m_rgb1 = m_start_c * shuffled_eye

        if not first:
            # fade from last rgb2 to start color
            print("rgb2 to start color")
            fade_colors(m_rgb2, m_start_c, num_sends, send_rate)
        else:
            first = False

        # more accurate time
        # for num_seconds seconds
        # end_time = time.time() + num_seconds
        # while (time.time() < end_time):

        # best effort time
        # fade from start color to rgb1
        print("start color to rgb1")
        fade_colors(m_start_c, m_rgb1, num_sends, send_rate)

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset

        shuffled_eye = create_shuffled_eye(NUM_PARS)

        # end_c = random_rgbw(reduce_w=True)
        end_c = pick_rgbw(reduce_w=False)
        print(end_c)
        m_end_c =  shuffled_eye.dot(np.tile(end_c, NUM_PARS).reshape(num_colors, NUM_PARS))
        m_rgb2 = m_end_c * shuffled_eye

        # fade from rgb1 to rgb2
        print("rgb1 to rgb2")
        fade_colors(m_rgb1, m_rgb2, num_sends, send_rate)

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset

        # fade from rgb2 to end color
        print("rgb2 to end color")
        fade_colors(m_rgb2, m_end_c, num_sends, send_rate)

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset

        # fade from end color to rgb2
        print("end color to rgb2")
        fade_colors(m_end_c, m_rgb2, num_sends, send_rate)

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset



def run_swirl(colors=((255, 165, 0, 0),(0, 0, 255, 0))):

    print("RUN SWIRL")

    NUM_PARS = 4
    step = 0.001

    i = -1
    t = np.linspace(0, 2*np.pi, 100)

    c1_val = 0.01
    c2_val = (NUM_PARS / 2.) + c1_val

    while True:

        next_preset = check_midi()
        if next_preset is not None:
            return next_preset

        i += 1
        if i >= len(t):
            i = 0
        if i + NUM_PARS <= len(t):
            t_cur = t[i:i+NUM_PARS]
        else:
            t_cur = t[i:] + t[:i+NUM_PARS-len(t)]


        # triang = sps.windows.triang(t_cur)

        m_c1 = np.tile(colors[0], (NUM_PARS, 1))
        m_c2 = np.tile(colors[1], (NUM_PARS, 1))

        c1_i1 = int(np.floor(c1_val))
        c1_i2 = int(np.ceil(c1_val))
        c1_v1 = c1_val - c1_i1
        c1_v2 = c1_i2 - c1_val
        c1_i2 %= NUM_PARS
        c1_diag = np.zeros(NUM_PARS)
        c1_diag[c1_i1] = c1_v1
        c1_diag[c1_i2] = c1_v2
        c1_diag  = np.diag(c1_diag)

        c2_i1 = int(np.floor(c2_val))
        c2_i2 = int(np.ceil(c2_val))
        c2_v1 = c2_val - c2_i1
        c2_v2 = c2_i2 - c2_val
        c2_i2 %= NUM_PARS
        c2_diag = np.zeros(NUM_PARS)
        c2_diag[c2_i1] = c2_v1
        c2_diag[c2_i2] = c2_v2
        c2_diag  = np.diag(c2_diag)

        m = (c1_diag.dot(m_c1) + c2_diag.dot(m_c2)).astype(int)

        set_segment_par(0, NUM_PARS, m[:,0], m[:,1], m[:,2], m[:,3])
        time.sleep(.05)

        c1_val += step
        c2_val += step

        if c1_val >= NUM_PARS:
            c1_val -= NUM_PARS

        if c2_val >= NUM_PARS:
            c2_val -= NUM_PARS

def run_manual():

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

        set_segment_par(0, NUM_PARS, c[:,0], c[:,1], c[:,2], c[:,3])

        time.sleep(.05)


presets = [
    run_manual,
    run_slowfade,
    run_separate,
    run_swirl
]

preset_idx = 0
def run_next(to_next=None):
    global preset_idx

    if to_next is None:
        return run_manual()
        # return run_swirl()
        # return run_slowfade()
        # return run_separate()
    elif to_next:
        preset_idx += 1
        if preset_idx == len(presets):
            preset_idx = 0
    else:
        preset_idx -= 1
        if preset_idx < 0:
            preset_idx = len(presets) -1

    return presets[preset_idx]()


to_next = None
while True:
    to_next = run_next(to_next)

