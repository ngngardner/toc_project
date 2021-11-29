"""Traffic flow module for core functions."""

from beartype import beartype

from traffic_sim.core.distance import euclidean
from traffic_sim.core.flow.base import FlowHelper


class TrafficFlow(FlowHelper):
    """A traffic flow represents a group of vehicles."""

    prev: tuple
    location: tuple
    dest: tuple
    volume: int
    possible_moves: dict

    def __str__(self) -> str:
        """
        Return a string representation of the flow.

        Returns:
            str: String representation of the flow.
        """
        res = {
            'previous': self.prev,
            'location': self.location,
            'dest': self.dest,
            'volume': self.volume,
        }
        return str(res)

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

    def renew_moves(self) -> None:
        """Renew the possible moves."""
        self.possible_moves = self.all_moves()

    @beartype
    def update_move(self, move: tuple, new: float) -> None:
        """Update the move.

        Args:
            move (tuple): The move to update.
            new (int): The value to update the move with.
        """
        self.possible_moves[move] = new

    @beartype
    def cost(self, move: tuple) -> float:
        """Get the cost of the move.

        Args:
            move (tuple): The move to get the cost of.

        Returns:
            float: The cost of the move.
        """
        return self.possible_moves[move]
