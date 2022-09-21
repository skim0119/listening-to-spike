"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import random
import time

from pythonosc import osc_message_builder, udp_client, osc_bundle_builder
from spike_load import signal_load


def test_run(ip, port):
    client = udp_client.SimpleUDPClient(ip, port)

    for x in range(10):
        client.send_message("/filter", random.random())
        time.sleep(1)


def run(path, ip, port):
    oscSender = udp_client.UDPClient(ip, port)
    rate, data = signal_load(path)

    stime = time.perf_counter()

    sample_nr = 0
    while True:
        offset = time.perf_counter() - stime
        sample_nr = int(offset * rate)

        # Stop if we pass data size
        if sample_nr >= data.shape[1]:
            break

        slices = data[:, sample_nr]

        bundle = osc_bundle_builder.OSCBundleBuilder(
            osc_bundle_builder.IMMEDIATELY
        )
        for ch in range(data.shape[0]):
            msg = osc_message_builder.OscMessageBuilder(
                address=f"/channel{ch}"
            )
            msg.add_arg(int(slices[ch]))
            bundle.add_content(msg.build())
            # oscSender.send(msg.build())

            bundle.add_content(bundle.build())
        oscSender.send(bundle.build())
