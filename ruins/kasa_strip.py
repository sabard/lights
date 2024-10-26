import sys

import asyncio
from kasa import SmartStrip

# LOCAL_IP = "172.17.3.20"
LOCAL_IP = "10.168.3.96"
LOCAL_IP = 192.168.0.1

# # Connect to kasa device wifi network
# # get device IP with:
# kasa discover
# # or
# ip route

# # get available wifi networks:
# kasa --host 192.168.0.1 wifi scan

# # join network
# kasa --host 192.168.0.1 wifi join <network-ssid>


async def on(num, ip=LOCAL_IP, verbose=True):
    p = SmartStrip(ip)

    # await p.update()  # Request the update
    await p.children[num].turn_on()


async def off(num, ip=LOCAL_IP, verbose=True):
    p = SmartStrip(ip)

    # await p.update()  # Request the update
    await p.children[num].turn_off()
