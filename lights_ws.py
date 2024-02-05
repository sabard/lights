import argparse
import json
import asyncio
from websockets.sync.client import connect

# WLED_ADDR = "ws://wled-stairs.local"
WLED_ADDR = "ws://wled-nook.local"


def on(ws):
    data = {"on": True}
    ws.send(json.dumps(data))


def off(ws):
    data = {"on": False}
    ws.send(json.dumps(data))


with connect(f"{WLED_ADDR}/ws") as ws:
    print("Enter commands:")
    while True:
        cmd = input()
        if cmd == "on":
            on(ws)
        elif cmd == "off":
            off(ws)
        else:
            break
