import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 21324

RESET_SEC = 10

def send_udp(data):
    m = []
    m.append(1)
    m.append(RESET_SEC)

    m.extend(data)

    m = bytes(m)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(m, (UDP_IP, UDP_PORT))
