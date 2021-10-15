"""Traffic simulator code."""

import logging
import sys
from os import path

from traffic_sim.matrix import TrafficMatrix
from traffic_sim.sim import TrafficSim

logger = logging.getLogger(__name__)

if not __package__:
    _path = path.realpath(path.abspath(__file__))
    sys.path.insert(0, path.dirname(path.dirname(_path)))


def init():
    """Initialize logging."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.info('Logging initialized.')


def main():
    """Run code from CLI."""
    # init logging
    init()

    # set traffic capacities (hardcoded)
    tm = TrafficMatrix(10, 10)
    tm.cmatrix[:, 2] = 2
    tm.cmatrix[:, 8] = 2
    tm.cmatrix[3, :] = 3
    tm.cmatrix[:, 5] = 4

    # simulate traffic
    sim = TrafficSim(tm)
    sim.run(10)
    sim.savefig('traffic_sim')


if __name__ == '__main__':
    main()
