"""Traffic simulator code."""

import sys
from os import path

from rich import inspect

from traffic_sim.console import console
from traffic_sim.matrix import WeightedMatrix
from traffic_sim.sim import TrafficSim

if not __package__:
    _path = path.realpath(path.abspath(__file__))
    sys.path.insert(0, path.dirname(path.dirname(_path)))


def main():
    """Run code from CLI."""
    console.log('traffic sim')

    # set traffic capacities (hardcoded)
    tm = WeightedMatrix(10, 10)
    tm.cmatrix[:, 2] = 2
    tm.cmatrix[:, 8] = 2
    tm.cmatrix[3, :] = 3
    tm.cmatrix[:, 5] = 4
    tm.set_weights()
    inspect(tm)

    # simulate traffic
    sim = TrafficSim(tm)
    sim.run(10)
    sim.savefig('traffic_sim')


if __name__ == '__main__':
    main()
