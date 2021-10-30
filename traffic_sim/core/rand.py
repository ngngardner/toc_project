"""Random module for core functions."""

from beartype import beartype
from numpy.random import Generator, default_rng


class RandomGenerator(object):
    """Base class with rng functionality."""

    seed: int
    rng: Generator

    @beartype
    def __init__(self, seed: int = 0):
        """Initialize the random number generator.

        Args:
            seed (int): [description]. Defaults to False.
        """
        if seed:
            self.rng = default_rng(seed)
        else:
            self.rng = default_rng()
        self.seed = seed
