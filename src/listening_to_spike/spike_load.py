import numpy as np
from miv.io import DataManager
from miv.signal.filter import ButterBandpass


def signal_load(path):  # TODO: read actual data
    filters = ButterBandpass(lowcut=300, highcut=3000, order=4)

    data = DataManager(path)[0]
    with data.load() as (signal, timestamps, sampling_rate):
        signal = filters(signal, sampling_rate)

    return sampling_rate, signal
