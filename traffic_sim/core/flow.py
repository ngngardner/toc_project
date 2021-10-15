"""Traffic flow module for core functions."""

from typing import List, Tuple

from traffic_sim.core.distance import euclidean


class TrafficFlow(object):
    """A traffic flow represents a group of vehicles."""

    location: tuple
    dest: tuple
    volume: int
    possible_moves: dict

    def __init__(
        self,
        location: tuple,
        dest: tuple,
        volume: int,
    ):
        """
        Initialize a traffic flow.

        Args:
            location (tuple): (row, col) of the current location.
            dest (tuple): (row, col) of the destination.
            volume (int): The volume of the flow.
        """
        self.location = location
        self.dest = dest
        self.volume = volume
        self.renew_moves()

    def all_moves(self) -> dict:
        """Calculate all possible moves.

        Returns:
            dict: Dictionary of possible moves with position as the key and
            distance as the value.
        """
        moves = {}
        pos = self.move_params()
        for diff_i in (-1, 0, 1):
            point = (pos[0] + diff_i, pos[1])
            moves[point] = euclidean(
                point, (pos[2], pos[3]),
            )

        for diff_j in (-1, 1):
            point = (pos[0], pos[1] + diff_j)
            moves[point] = euclidean(
                point, (pos[2], pos[3]),
            )
        return moves

    def renew_moves(self):
        """Renew the possible moves."""
        self.possible_moves = self.all_moves()

    def move_params(self) -> Tuple[int, int, int, int]:
        """
        Return the current location and destination.

        Returns:
            Tuple[int, int, int, int]: (row, col, row, col) of current location
            and desination.
        """
        loc_x, loc_y = self.location
        dest_x, dest_y = self.dest
        return loc_x, loc_y, dest_x, dest_y

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
        self.location = min(self.possible_moves, key=self.possible_moves.get)

    def is_complete(self) -> bool:
        """
        Check if the flow is complete.

        Returns:
            bool: True if the flow is complete, False otherwise.
        """
        return self.location == self.dest
