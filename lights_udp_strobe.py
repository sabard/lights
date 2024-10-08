import numpy as np
from pynput import keyboard
import pygame
import pygame.midi
import socket
import time

# UDP_IP = "wled-stairs.local"
# UDP_IP = "127.0.0.1"
# UDP_IP = "172.17.2.73"  # stairs
# UDP_IP = "172.17.2.71"
UDP_IP = "172.17.2.72"  # nook

UDP_IP = "4.3.2.1"

UDP_PORT = 21324

RESET_SEC = 10

PYGAME_MIDI_DEVICE=0

SEND_RATE = 30  # Hz
SEND_PERIOD = 1. / SEND_RATE

segment_chars = "qwertyuiop"
num_leds = 120
leds_per_key = num_leds // len(segment_chars)


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


def set_segment(start, end, r, g, b):
    m = []
    m.append(1)
    m.append(10)

    for i in range(start, end):
        m.append(i)  # Index of pixel to change
        m.append(r)  # Pixel red value
        m.append(g)  # Pixel green value
        m.append(b)  # Pixel blue value

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (UDP_IP, UDP_PORT))


# assumes both data specify same leds
def combine_data(d1, d2):
    assert(len(d1) == len(d2))

    d = []

    for i in range(0, len(d1), 4):
        assert(d1[i] == d2[i])
        d.append(d1[i])
        d.append(d1[i + 1] + d2[i + 1])
        d.append(d1[i + 2] + d2[i + 2])
        d.append(d1[i + 3] + d2[i + 3])

    return d


def send_udp(data):
    m = []
    m.append(1)
    m.append(RESET_SEC)

    m.extend(data)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (UDP_IP, UDP_PORT))

def on_press(key):
    try:
        c = key.char
    except AttributeError:
        return
    if c not in segment_chars:
        return


def on_release(key):
    try:
        c = key.char
    except AttributeError:
        return
    if c not in segment_chars:
        return


mIn = MidiKeyboard()

# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()

ts = {
    "red": 0,
    "green": 0,
    "blue": 0,
}
vals = {
    "red": 0,
    "green": 0,
    "blue": 0,
}
dts = {
    "red": SEND_PERIOD,
    "green": SEND_PERIOD,
    "blue": SEND_PERIOD,
}
directions = {
    "red": 1,
    "green": 1,
    "blue": 1,
}

toggle = 0

while True:
    if mIn.midiDevice:
        if mIn.midiDevice.poll():
            events = mIn.midiDevice.read(100)
            ev_data = events[-1][0] # only use last event
            button = ev_data[1]
            ev_value = ev_data[2]
            print(events)

            if button == 3:  # red intensity
                vals["red"] = ev_value * 2
            elif button == 4:  # green intensity
                vals["green"] = ev_value * 2
            elif button == 5:  # blue intensity
                vals["blue"] = ev_value * 2

            if button == 14:  # red freq
                dts["red"] = ev_value / 127. / 3.
            elif button == 15:  # green freq
                dts["green"] = ev_value / 127. / 3.
            elif button == 16:  # blue freq
                dts["blue"] = ev_value / 127. / 3.

            if button == 23:  # red direction
                if ev_value == 127:
                    directions["red"] *= -1
            elif button == 24:  # green direction
                if ev_value == 127:
                    directions["green"] *= -1
            elif button == 25:  # blue direction
                if ev_value == 127:
                    directions["blue"] *= -1
    else:
        time.sleep(.01)

    if toggle == 1:
        toggle = 0
        set_segment(0, 120, 0, 0, 0)
        # print("set off")
    elif toggle == 0:
        toggle = 1
        val = int(np.random.random() * 255)
        set_segment(0, 120, val, val, val)
        # print("set on")

    time.sleep(SEND_PERIOD)
