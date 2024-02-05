from pynput import keyboard
import socket

# UDP_IP = "wled-stairs.local"
# UDP_IP = "172.17.2.73"
UDP_IP = "172.17.2.72"
UDP_PORT = 21324

segment_chars = "qwertyuiop"
num_leds = 120
leds_per_key = num_leds // len(segment_chars)


def set_segment(start, end, val):
    m = []
    m.append(1)
    m.append(10)

    for i in range(start, end):
        m.append(i)  # Index of pixel to change
        m.append(val)  # Pixel red value
        m.append(0)  # Pixel green value
        m.append(0)  # Pixel blue value

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

    start_idx = segment_chars.index(c) * leds_per_key
    end_idx = start_idx + leds_per_key
    set_segment(start_idx, end_idx, 50)


def on_release(key):
    try:
        c = key.char
    except AttributeError:
        return
    if c not in segment_chars:
        return

    start_idx = segment_chars.index(c) * leds_per_key
    end_idx = start_idx + leds_per_key
    set_segment(start_idx, end_idx, 0)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
