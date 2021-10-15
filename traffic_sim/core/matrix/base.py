"""Base class for traffic matrix operations."""

from typing import Optional, Tuple

import numpy as np

from traffic_sim.core.rand import RandomGenerator


class MatrixHelper(RandomGenerator):
    """Matrix helper class."""

    rows: int
    cols: int
    cmatrix: np.ndarray
    vmatrix: np.ndarray

    def __init__(
        self,
        rows: int,
        cols: int,
        seed: Optional[int] = None,
    ):
        """Initialize matrix helper class.

        Args:
            rows (int): Number of rows in matrix.
            cols (int): Number of columns in matrix.
            seed (int, optional): Random seed. Defaults to None.
        """
        super().__init__(seed)
        self.rows = rows
        self.cols = cols

        # capacity and volume matrix
        self.cmatrix = np.zeros((rows, cols), dtype=int)
        self.vmatrix = np.zeros((rows, cols), dtype=int)

    def clear_volume(self) -> None:
        """Clear traffic volume matrix."""
        self.vmatrix = np.zeros((self.rows, self.cols), dtype=int)

    def capacity(self, pos: tuple) -> int:
        """Return traffic cell capacity given a position.

        Args:
            pos (tuple): Position of traffic cell.

        Returns:
            int: Traffic cell capacity.
        """
        return self.cmatrix[pos]

    def volume(self, pos: tuple) -> int:
        """Return traffic cell volume given a position.

        Args:
            pos (tuple): Position of traffic cell.

        Returns:
            int: Traffic cell volume.
        """
        return self.vmatrix[pos]

    def is_valid(self, pos: tuple) -> bool:
        """Return if position is valid (within bounds).

        Args:
            pos(tuple): Position to check.

        Returns:
            bool: If position is within bounds.
        """
        in_row = 0 <= pos[0] < self.rows
        in_col = 0 <= pos[1] < self.cols
        return in_row and in_col

    def is_full(self, pos: tuple) -> bool:
        """Check a traffic cell is full(volume exceeds capacity).

        Args:
            pos(tuple): Position to check.

        Returns:
            bool: If traffic cell is full.
        """
        if not self.is_valid(pos):
            return False

        return self.volume(pos) >= self.capacity(pos)

    def select_cells(self, num_cells: int) -> Tuple[np.ndarray, np.ndarray]:
        """Randomly choose 'num_cells' cells for creating traffic flows.

        Args:
            num_cells(int): Number of cells to select.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Tuple of selected cells as cartesian
            coordinates with x-values in the first element and y-values in the
            second element.
        """
        # select cells with traffic capacity
        idxs = np.where(self.cmatrix > 0)

        # select num_cells cells randomly
        possible_idxs = range(len(idxs[0]))
        chosen_idxs = self.rng.choice(possible_idxs, num_cells, replace=False)

        # return selected cells
        x_idxs = np.array(idxs[0])[chosen_idxs]
        y_idxs = np.array(idxs[1])[chosen_idxs]

        return (x_idxs, y_idxs)
