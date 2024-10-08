from pynput import keyboard
import pygame
import pygame.midi
import socket
import time

UDP_IP1 = "4.3.2.1"

# UDP_IP = "wled-stairs.local"
# home
# UDP_IP1 = "127.0.0.1"
# UDP_IP = "172.17.2.73" # stairs
# UDP_IP1 = "172.17.2.71"  # hall
# UDP_IP1 = "172.17.2.72"  # nook
# UDP_IP2 = "172.17.2.74"  # bed

# studio
# UDP_IP1 = "172.17.3.41"  # strip
# UDP_IP1 = "172.17.3.43"  # par

UDP_PORT = 21324
# UDP_PORT = 21325

TIMEOUT = 10
PYGAME_MIDI_DEVICE=0

segment_chars = "qwertyuiopasdfghjkl"
num_leds = 240

# segment_chars = "qwertyuiop"
# num_leds = 120

# num_leds = 16
# segment_chars = "qwertyuiasdfghjk"

# num_leds = 8
# segment_chars = "qwertyui"

# num_leds = 4
# segment_chars = "qwer"

leds_per_key = num_leds // len(segment_chars)

red_val = 0
green_val = 0
blue_val = 0


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


def set_segment(start, end, r, g, b):
    m = []
    m.append(1)
    m.append(TIMEOUT)

    for i in range(start, end):
        m.append(i)  # Index of pixel to change
        m.append(r)  # Pixel red value
        m.append(g)  # Pixel green value
        m.append(b)  # Pixel blue value

    print(m)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (UDP_IP1, UDP_PORT))
    # sock.sendto(m, (UDP_IP2, UDP_PORT))


def on_press(key):
    global red_val, green_val, blue_val

    try:
        c = key.char
    except AttributeError:
        return
    if c and c not in segment_chars:
        return

    start_idx = segment_chars.index(c) * leds_per_key
    end_idx = start_idx + leds_per_key
    print("on: ", start_idx, end_idx)
    set_segment(start_idx, end_idx, red_val, green_val, blue_val)


def on_release(key):
    try:
        c = key.char
    except AttributeError:
        return
    if c and c not in segment_chars:
        return

    start_idx = segment_chars.index(c) * leds_per_key
    end_idx = start_idx + leds_per_key
    print("off: ", start_idx, end_idx)
    set_segment(start_idx, end_idx, 0, 0, 0)


mIn = MidiKeyboard()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

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
    else:
        time.sleep(1)
