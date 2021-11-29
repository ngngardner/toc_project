"""Traffic simulator code."""

import sys
from os import path

from traffic_sim.analysis import TrafficExperiment
from traffic_sim.console import console

if not __package__:
    _path = path.realpath(path.abspath(__file__))
    sys.path.insert(0, path.dirname(path.dirname(_path)))


def main():
    """Run code from CLI."""
    console.log('traffic sim')
    num_trials = 30
    ex = TrafficExperiment(
        experiments=100,
        trials=num_trials,
        rows=10,
        cols=10,
        epochs=10,
    )
    ex.run()
    ex.analyze()


if __name__ == '__main__':
    main()
