"""Traffic matrix module for core functions."""

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np

from traffic_sim.core.distance import coord_list
from traffic_sim.core.flow import TrafficFlow
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

        # set traffic capacities (hardcoded)
        self.cmatrix[:, 2] = 2
        self.cmatrix[:, 8] = 2
        self.cmatrix[3, :] = 3
        self.cmatrix[:, 5] = 4

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


@dataclass
class TrafficMatrix(MatrixHelper):
    """Traffic matrix class for running main algorithm."""

    rows: int
    cols: int
    cmatrix: np.ndarray
    vmatrix: np.ndarray
    density: float
    flows: List[TrafficFlow]

    def __init__(
        self,
        rows: int,
        cols: int,
        density: Optional[float] = 0.05,
        seed: Optional[int] = None,
    ):
        """Initialize a traffic simulation object.

        Args:
            rows (int): Number of rows in the traffic matrix.
            cols (int): Number of columns in the traffic matrix.
            density (Optional[float]): Density of traffic flow simulation.
            seed (Optional[int], optional): Random seed.
        """
        super().__init__(rows, cols, seed)
        self.density = density
        self.flows = []

    def run(self, iterations: int) -> None:
        """Run the traffic simulation.

        Args:
            iterations (int): Number of iterations to run.
        """
        for _ in range(iterations):
            self.generate_flows()
            self.step_flows()
            self.update_matrix()
            self.pop_flows()

    def generate_flows(self) -> None:
        """
        Generate traffic flows based on density.

        Returns:
            None
        """
        num_cells = self.rows * self.cols * self.density
        num_cells = round(num_cells) - len(self.flows)
        if num_cells <= 0:
            # no new flows to generate, so return
            return None

        # create flow origins and destinations
        origins = coord_list(self.select_cells(num_cells))
        dests = coord_list(self.select_cells(num_cells))

        for idx in range(num_cells):
            # volume of the flow is a random number between 1 and capacity-1
            capacity = self.capacity(origins[idx])
            volume = self.rng.choice(range(1, capacity))

            flow = TrafficFlow(origins[idx], dests[idx], volume)
            self.flows.append(flow)

    def step_flows(self) -> None:
        """Get the next move for every flow and execute."""
        for flow in self.flows:
            moves = flow.moves_list()
            for move in moves:
                if not self.is_valid(move) or self.is_full(move):
                    flow.unset_move(move)
            flow.step()

    def pop_flows(self) -> None:
        """Remove completed flows."""
        self.flows = [flow for flow in self.flows if not flow.is_complete()]

    def update_matrix(self) -> None:
        """Update traffic volume matrix based on current flows."""
        self.vmatrix = np.zeros(self.vmatrix.shape, dtype=int)

        for flow in self.flows:
            location = flow.location
            volume = flow.volume
            self.vmatrix[location] += volume
