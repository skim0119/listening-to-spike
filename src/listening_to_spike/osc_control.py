"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import random
import time

from pythonosc import udp_client
from spike_load import signal_load


def run(path, ip, port):
    signal = signal_load(path)

    client = udp_client.SimpleUDPClient(ip, port)

    for x in range(10):
        client.send_message("/filter", random.random())
        time.sleep(1)
