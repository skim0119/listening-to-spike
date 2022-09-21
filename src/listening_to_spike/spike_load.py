import numpy as np
from miv import datasets


def signal_load(path):  # TODO: read actual data
    experiments = datasets.optogenetic.load_data()
    experiments.tree()

    return 30_000, np.random.random(100, 40)
