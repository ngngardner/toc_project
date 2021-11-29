"""A traffic matrix that implements directional cells."""

import numpy as np
from beartype import beartype

from traffic_sim.core.matrix.traffic import TrafficMatrix


class DirectedMatrix(TrafficMatrix):
    """Directed traffic matrix."""

    dmatrix: np.ndarray

    @beartype
    def __init__(
        self,
        rows: int,
        cols: int,
        density: float = 0.05,
        seed: int = 0,
    ):
        """Initialize a directed traffic matrix.

        dmatrix is a numpy array of shape (rows, cols, 2) where the first
        dimension is the row and the second dimension is the column. The third
        dimension is a tuple of the allowed directions of the form (up, down,
        left, right). 1 indicates that traffic flows in that cell can move in
        that direction. 0 indicates that traffic can't move in that direction.

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
            density (float): Traffic density. Defaults to 0.05.
            seed (int): Random seed. Defaults to None.
        """
        super().__init__(rows, cols, density, seed)
        self.dmatrix = np.zeros((rows, cols, 4), dtype=bool)

    @beartype
    def set_direction(
        self,
        pos: tuple[int, int],
        dirs: tuple[bool, bool, bool, bool],
    ) -> None:
        """Set direction and location of traffic
        
        Args:
            pos (tuple): Location of traffic. Tuple of length 2 of the
            form (row, col).
            dirs (tuple): Direction of traffic. Tuple of length 4 of the
            form (up, down, left, right).
        """
        self.dmatrix[pos] = dirs


    @beartype
    def set_row(self, row: int, dirs: tuple[bool, bool, bool, bool]) -> None:
        """Set the row of the directed matrix.

        Args:
            row (int): Row index.
            dirs (tuple): Direction of traffic. Tuple of length 4 of the
            form (up, down, left, right).
        """
        for col in range(self.cols):
            self.set_direction((row, col), dirs)
        
    @beartype
    def set_col(self, col: int, dirs: tuple[bool, bool, bool, bool]) -> None:
        """Set the column of the directed matrix
        
        Args:
            col (int): Column index.
            dirs (tuple): Direction of traffic. Tuple of length 4 of the
            form (up, down, left, right).
        """
        for row in range(self.rows):
            self.set_direction((row, col), dirs)

    @beartype
    def get_direction(
        self,
        pos: tuple[int, int],
    ) -> tuple[bool, bool, bool, bool]:
        """Return the direction and location of traffic.

        Args:
            pos (tuple): Location of the cell in the matrix.
        
        Returns:
            tuple: Direction of traffic. Tuple of length 4 of the form
            (up, down, left, right).
        """
        return self.dmatrix[pos]

    def step_flows(self) -> None:
        """Step each flow in directed matrix"""
        for flow in self.flows:
            flow.renew_moves()
            moves = flow.moves_list()
            for move in moves:
                if not self.is_valid(move) or self.is_full(move):
                    flow.unset_move(move)
                dirs = self.get_direction(flow.location)
                row_diff = flow.location[0] - move[0]
                col_diff = flow.location[1] - move[1]
                
                # Up
                if row_diff == -1 and not dirs[0]:
                    flow.unset_move(move)
                # Down
                elif row_diff == 1 and not dirs[1]:
                    flow.unset_move(move)
                # Left
                elif col_diff == -1 and not dirs[2]:
                    flow.unset_move(move)
                # Right
                elif col_diff == 1 and not dirs[3]:
                    flow.unset_move(move)
            flow.step()

