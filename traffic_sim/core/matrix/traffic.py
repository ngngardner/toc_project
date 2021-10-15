"""Traffic matrix class for running simulation algorithm."""

from typing import List, Optional

import numpy as np

from traffic_sim.core.distance import coord_list
from traffic_sim.core.flow import TrafficFlow
from traffic_sim.core.matrix.base import MatrixHelper


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

    def step(self) -> None:
        """Step through the traffic simulation."""
        self.generate_flows()
        self.step_flows()
        self.update_matrix()
        self.pop_flows()

    

    def generate_flows(self) -> None:
        """Generate traffic flows based on density."""
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
            flow.renew_moves()
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
