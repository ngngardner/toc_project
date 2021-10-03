"""Traffic simulator code."""

import logging
import sys
from os import path

from traffic_sim.core import example

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
    init()
    example('test')


if __name__ == '__main__':
    main()
