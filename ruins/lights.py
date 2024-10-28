import socket

from collections.abc import Iterable

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

class DmxChain:
    def __init__(self, num_lights, ip, port, timeout=10):
        self.num_lights = num_lights
        self.ip = ip
        self.port = port
        self.timeout = timeout
        # self.protocol = "DRGBW" # TODO make enum

    def set_segment(self, start, end, r, g, b, w, print_packet=False):
        m = []
        m.append(3) # DRGBW
        m.append(self.timeout)

        for i in range(start, end):
            # m.append(i)  # Index of pixel to change

             # pixel red value
            if isinstance(r, Iterable):
                if r[i] > 255:
                    r[i] = 255
                if r[i] < 0:
                    r[i] = 0
                m.append(r[i])
            else:
                if r > 255:
                    r = 255
                if r < 0:
                    r = 0
                m.append(r)

            # pixel green value
            if isinstance(g, Iterable):
                if g[i] > 255:
                    g[i] = 255
                if g[i] < 0:
                    g[i] = 0
                m.append(g[i])
            else:
                if g > 255:
                    g = 255
                if g < 0:
                    g = 0
                m.append(g)

            # pixel blue value
            if isinstance(b, Iterable):
                if b[i] > 255:
                    b[i] = 255
                if b[i] < 0:
                    b[i] = 0
                m.append(b[i])
            else:
                if b > 255:
                    b = 255
                if b < 0:
                    b = 0
                m.append(b)

            # pixel white value
            if isinstance(w, Iterable):
                if w[i] > 255:
                    w[i] = 255
                if w[i] < 0:
                    w[i] = 0
                m.append(w[i])
            else:
                if w > 255:
                    w = 255
                if w < 0:
                    w = 0
                m.append(w)

        if print_packet:
            print(m)

        m = bytes(m)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(m, (self.ip, self.port))
