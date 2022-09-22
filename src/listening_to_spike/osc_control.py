import random
import time
import numpy as np

from pythonosc import osc_message_builder, udp_client, osc_bundle_builder
from listening_to_spike.spike_load import signal_load


def test_run(ip, port):
    client = udp_client.SimpleUDPClient(ip, port)

    for x in range(10):
        client.send_message("/filter", random.random())
        time.sleep(1)


def run(path, ip, port):
    oscSender = udp_client.SimpleUDPClient(ip, port)
    rate, data = signal_load(path)

    sample_nr = 0
    nrs = []
    _data = []
    stime = time.perf_counter()
    while True:
        offset = time.perf_counter() - stime
        sample_nr = int(offset * rate)
        nrs.append(sample_nr)

        # Stop if we pass data size
        if sample_nr >= data.shape[0]:
            break

        slices = data[sample_nr, :]

        bundle = osc_bundle_builder.OscBundleBuilder(
            osc_bundle_builder.IMMEDIATELY
        )
        for ch in range(data.shape[1]):
            if ch == 0:
                _data.append(slices[ch])
            msg = osc_message_builder.OscMessageBuilder(
                address=f"/channel/{ch}"
            )
            msg.add_arg(arg_value=slices[ch], arg_type="f")
            bundle.add_content(msg.build())
        oscSender.send(bundle.build())

        time.sleep(0.0025)  # Control frequency

    oscSender.send_message(
        "/analysis/rate_average", (rate / np.diff(nrs)).mean()
    )
    oscSender.send_message(
        "/analysis/rate_deviation", (rate / np.diff(nrs)).std()
    )
    oscSender.send_message(
        "/analysis/total_playtime", time.perf_counter() - stime
    )
