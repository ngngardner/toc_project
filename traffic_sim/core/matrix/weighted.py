from typing import List, Optional

import numpy as np

from traffic_sim.core.matrix.traffic import TrafficMatrix

class WeightedMatrix(TrafficMatrix):
    """"""
    wmatrix: np.ndarray

    def __init__(
        self,
        rows: int,
        cols: int,
        density: Optional[float] = 0.05,
        seed: Optional[int] = None,
    ):
        super().__init__(rows, cols, density, seed)
        self.wmatrix = np.zeros((rows, cols), dtype=np.float64)

    def set_weights(self) -> None:
        """Set traffic cell weights to be the inverse of capacity."""
        self.wmartix = np.reciprocal(self.cmatrix+1, dtype=np.float64)

    def step_flows(self) -> None:
        for flow in self.flows:
            flow.renew_moves()
            moves = flow.moves_list()
            for move in moves:
                if not self.is_valid(move) or self.is_full(move):
                    flow.unset_move(move)
                else:
                    flow.update_move(move, flow.cost(move) * self.weight(move))
            flow.step()

    def weight(self, pos: tuple) -> int:
        """Return traffic cell weight given a position.

        Args:
            pos (tuple): Position of traffic cell.

        Returns:
            int: Traffic cell weight.
        """
        return self.wmatrix[pos]