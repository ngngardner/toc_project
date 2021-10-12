"""Random module for core functions."""

from typing import Optional

from numpy.random import Generator, default_rng


class RandomGenerator(object):
    """Base class with rng functionality."""

    seed: Optional[int]
    rng: Generator

    def __init__(self, seed=0):
        """Initialize the random number generator.

        Args:
            seed (bool, optional): [description]. Defaults to False.
        """
        if seed:
            self.rng = default_rng(seed)
        else:
            self.rng = default_rng()
        self.seed = seed
