
def run_swirl(colors=((255, 165, 0)),(0, 0, 255))):
    while True:
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
