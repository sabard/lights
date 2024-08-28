from collections.abc import Iterable
import numpy as np
from pynput import keyboard
import pygame
import pygame.midi
import socket
import time
from scipy import signal as sps

# from .swirl import run_swirl

# local
STRIP_IP = "127.0.0.1"
STRIP_PORT = 21324

PAR_IP = "127.0.0.1"
PAR_PORT = 21325

# studio
# STRIP_IP = "172.17.3.41"
# STRIP_PORT = 21324

# PAR_IP = "172.17.3.43"
# PAR_PORT = 21324

TIMEOUT = 2
PYGAME_MIDI_DEVICE=0

num_pars = 4

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
                self.midiDevice = pygame.midi.Input(PYGAME_MIDI_DEVICE, 100)

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


def set_segment_strip(start, end, r, g, b, print_packet=False):#, w):
    m = []
    m.append(1) # WARLS
    m.append(TIMEOUT)

    for i in range(start, end):
        m.append(i)  # Index of pixel to change

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
    end_idx = num_pars - 1
    print("on: ", start_idx, end_idx)
    set_segment_par(start_idx, end_idx, red_val, green_val, blue_val, white_val)


def on_release(key):
    try:
        c = key.char
    except AttributeError:
        return

    start_idx = 0
    end_idx = num_pars - 1
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

def run_slowfade():
    global i,j,k,signal

    while True:
        if mIn.midiDevice:
            if mIn.midiDevice.poll():
                events = mIn.midiDevice.read(1)
                ev_data = events[0][0]
                button = ev_data[1]
                ev_value = ev_data[2]

                if button == 14:
                    red_val = ev_value * 2
                elif button == 15:
                    green_val = ev_value * 2
                elif button == 16:
                    blue_val = ev_value * 2
                elif button == 17:
                    white_val = ev_value * 2
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
            set_segment_par(0, num_pars, red_val, green_val, blue_val, white_val)
            time.sleep(.05)


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

def random_rgbw(max_val=255, white=False):
    white_val = random_color(max_val) if white else 0
    return np.array([
            random_color(max_val), # r
            random_color(max_val), # g
            random_color(max_val), # b
            white_val # w
        ])

def calculate_color(m1, m2, i, num_sends):
    return (m1 - (m1 - m2) * 1. * i / num_sends).astype(int)

def fade_colors(m1, m2, num_sends, send_rate):
    for i in range(num_sends):
        # calculate color
        c = calculate_color(m1, m2, i, num_sends)

        # send color
        set_segment_par(0, num_pars, c[:,0], c[:,1], c[:,2], c[:,3])

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


def run_separate(num_seconds=10, send_rate=.2):

    num_sends = int(1.0 * num_seconds / send_rate)
    num_colors = 4 # rgbw

    shuffled_eye = create_shuffled_eye(num_pars)

    first = True
    m_rgb2 = None

    while True:
        # pick color
        start_c = random_rgbw()
        m_start_c = np.tile(start_c, num_pars).reshape(num_colors, num_pars).dot(shuffled_eye)
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

        shuffled_eye = create_shuffled_eye(num_pars)

        end_c = random_rgbw()
        m_end_c =  np.tile(end_c, num_pars).reshape(num_colors, num_pars).dot(shuffled_eye)
        m_rgb2 = m_end_c * shuffled_eye

        # fade from rgb1 to rgb2
        print("rgb1 to rgb2")
        fade_colors(m_rgb1, m_rgb2, num_sends, send_rate)

        # fade from rgb2 to end color
        print("rgb2 to end color")
        fade_colors(m_rgb2, m_end_c, num_sends, send_rate)

        # fade from end color to rgb2
        print("end color to rgb2")
        fade_colors(m_end_c, m_rgb2, num_sends, send_rate)



def run_swirl(colors=((255, 165, 0, 0),(0, 0, 255, 0))):
    num_pars = 4
    step = 0.001

    i = -1
    t = np.linspace(0, 2*np.pi, 100)

    c1_val = 0.01
    c2_val = (num_pars / 2.) + c1_val

    while True:
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

        set_segment_par(0, num_pars, m[:,0], m[:,1], m[:,2], m[:,3])
        time.sleep(.05)

        c1_val += step
        c2_val += step

        if c1_val >= num_pars:
            c1_val -= num_pars

        if c2_val >= num_pars:
            c2_val -= num_pars


# run_slowfade()
run_separate()
# run_swirl()

