"""Traffic flow module for core functions."""

from dataclasses import dataclass
from typing import List, Tuple

from traffic_sim.core.distance import euclidean


@dataclass
class TrafficFlow(object):
    """A traffic flow represents a group of vehicles."""

    location: tuple
    dest: tuple
    capacity: int
    possible_moves: dict

    def __init__(self, location: tuple, dest: tuple, capacity: int):
        """
        Initialize a traffic flow.

        Args:
            location (tuple): (row, col) of the current location.
            dest (tuple): (row, col) of the destination.
            capacity (int): The maximum capacity of the flow.
        """
        self.location = location
        self.dest = dest
        self.capacity = capacity
        self.possible_moves = self.all_moves()

    def all_moves(self) -> None:
        """Calculate all possible moves."""
        loc_x, loc_y, dest_x, dest_y = self.get_move_params()
        for diff_i in range(-1, 2):
            for diff_j in range(-1, 2):
                point = (loc_x + diff_i, loc_y + diff_j)
                self.possible_moves[point] = euclidean(
                    point, (dest_x, dest_y),
                )

    def move_params(self) -> Tuple[int, int, int, int]:
        """
        Return the current location and destination.

        Returns:
            Tuple[int, int, int, int]: (row, col, row, col) of current location
            and desination.
        """
        return self.location, self.dest

    def moves_list(self) -> List[tuple]:
        """
        Return a list of possible moves.

        Returns:
            List[tuple]: List of possible moves.
        """
        return list(self.possible_moves.keys())

    def unset_move(self, move: tuple) -> None:
        """
        Given a move, remove it as a possible move(due to full capacity).

        Args:
            move (tuple): (row, col) of the move to remove.
        """
        self.possible_moves.pop(move)

    def step(self) -> None:
        """
        Calculate the next step to move.

        Move from the current location to the destination and update the
        current location.
        """
        self.location = min(self.moves_list())
