"""Traffic simulator code."""

import logging
import sys
from os import path

from traffic_sim.core.matrix import TrafficMatrix

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

    # traffic matrix
    tm = TrafficMatrix(10, 10)
    tm.run(5)


if __name__ == '__main__':
    main()
