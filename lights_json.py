import argparse
import json
import requests

# WLED_ADDR = "http://wled-stairs.local"
WLED_ADDR = "http://wled-nook.local"

r = requests.get(f"{WLED_ADDR}/json")
# print(r.json())


def on():
    data = {"on": True}
    r = requests.post(f"{WLED_ADDR}/json/state", data=json.dumps(data))


def off():
    data = {"on": False}
    r = requests.post(f"{WLED_ADDR}/json/state", data=json.dumps(data))


def main():
    parser = argparse.ArgumentParser(
        prog="lights-control",
        description="Control WLED lights via JSON API"
    )
    parser.add_argument("cmd", type=str, choices=["on", "off"])

    args = parser.parse_args()
    if args.cmd == "on":
        on()
    elif args.cmd == "off":
        off()


if __name__ == "__main__":

    main()
