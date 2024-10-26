# from pynput import keyboard

red_val = 255
green_val = 0
blue_val = 0
white_val = 255

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


# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
