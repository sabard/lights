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
        sock.sendto(m, (self.ip, self.port))
