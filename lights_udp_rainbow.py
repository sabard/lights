from colormath import color_objects, color_conversions
import numpy as np
import pygame
import pygame.midi
import socket
import time

# UDP_IP = "wled-stairs.local"
UDP_IP = "127.0.0.1"
# UDP_IP = "172.17.2.73"  # stairs
# UDP_IP = "172.17.2.71"
# UDP_IP = "172.17.2.72"  # nook
UDP_PORT = 21324

RESET_SEC = 10

PYGAME_MIDI_DEVICE=0

SEND_RATE = 20  # Hz
SEND_PERIOD = 1. / SEND_RATE

SPEC_MIN = 340
SPEC_MAX = 830
SPEC_STEP = 10
SPEC_TOTAL_MIN = 340
SPEC_TOTAL_MIN = 830
SPEC_TOTAL_STEPS = (830 - 340) // SPEC_STEP
SPEC_NUM_STEPS = (SPEC_MAX - SPEC_MIN) // SPEC_STEP

num_leds = 147

class MidiKeyboard():
    def __init__(self):
        try:
            pygame.init()
            pygame.midi.init()

            if pygame.midi.get_count() < 1:
                print('Midi board not found!\n')
                self.midiDevice = None
            else:
                self.midiDevice = pygame.midi.Input(PYGAME_MIDI_DEVICE, 100)

        except Exception as e:
            print(e)


def spectral_to_rgb(freq):
    args = [0] * SPEC_TOTAL_STEPS
    args[(freq - SPEC_TOTAL_MIN) // SPEC_STEP] = 1000000.
    spectral_color = color_objects.SpectralColor(*args)
    rgb_color = color_conversions.convert_color(
        spectral_color, color_objects.sRGBColor
    )
    return int(rgb_color.rgb_r), int(rgb_color.rgb_g), int(rgb_color.rgb_b)


def construct_segment(start, end, r, g, b):
    d = []

    for i in range(start, end):
        d.append(i)  # Index of pixel to change
        d.append(r)  # Pixel red value
        d.append(g)  # Pixel green value
        d.append(b)  # Pixel blue value

    return d


def construct_sine_data(start, end, t, r, g, b):
    d = []

    x = np.linspace(-np.pi + t, np.pi + t, 120)
    vals = (np.sin(x) + 1.) / 2.

    for i in range(start, end):
        d.append(i)  # Index of pixel to change
        d.append(int(r * vals[i]))  # Pixel red value
        d.append(int(g * vals[i]))  # Pixel green value
        d.append(int(b * vals[i]))  # Pixel blue value

    return d


# assumes both data specify same leds
def combine_data(d1, d2):
    d = []
    d_dict = {}
    for i in range(0, len(d1), 4):
        d_dict[d1[i]] = (d1[i+1], d1[i+2], d1[i+3])

    for i in range(0, len(d2), 4):
        if d_dict.get(d2[i]):
            r, g, b = d_dict[d2[i]]
            d_dict[d2[i]] = (r + d2[i+1], g + d2[i+2], b + d2[i+3])
        else:
            d_dict[d2[i]] = (d2[i+1], d2[i+2], d2[i+3])

    for k, v in d_dict.items():
        d.append(k)
        d.append(v[0])
        d.append(v[1])
        d.append(v[2])

    return d


def send_udp(data):
    m = []
    m.append(1)
    m.append(RESET_SEC)

    m.extend(data)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (UDP_IP, UDP_PORT))


mIn = MidiKeyboard()

freqs = np.arange(SPEC_MIN, SPEC_MAX, SPEC_STEP)
freq_idx = 0

mode = 0
data = []
shift = 0

while True:
    if mIn.midiDevice:
        if mIn.midiDevice.poll():
            events = mIn.midiDevice.read(1)
            ev_data = events[0][0]
            button = ev_data[1]
            ev_value = ev_data[2]

    if mode == 0:
        r, g, b = spectral_to_rgb(freqs[freq_idx])
        data = construct_segment(0, num_leds, r, g, b)
    elif mode == 1:
        data = []
        for i in range(SPEC_NUM_STEPS): # +1
            f = (SPEC_MIN + (i + shift) * SPEC_STEP) % SPEC_MAX
            r, g, b = spectral_to_rgb(f)
            num_segment_leds = int(num_leds / SPEC_NUM_STEPS)
            start = i * num_segment_leds
            end = i * num_segment_leds + num_segment_leds
            seg_data = construct_segment(start, end, r, g, b)
            data = combine_data(data, seg_data)
        shift -= 1
    send_udp(data)

    freq_idx += 1
    if freq_idx >= len(freqs):
        freq_idx = 0

    time.sleep(SEND_PERIOD)
