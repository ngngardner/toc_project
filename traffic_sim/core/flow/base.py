"""Base class for traffic flow operations."""

from beartype import beartype


class FlowHelper(object):
    """Flow helper class."""

    prev: tuple
    location: tuple
    dest: tuple
    volume: int
    possible_moves: dict

    @beartype
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

    @beartype
    def move_params(self) -> tuple[int, int, int, int]:
        """
        Return the current location and destination.

        Returns:
            Tuple[int, int, int, int]: (row, col, row, col) of current location
            and desination.
        """
        loc_x, loc_y = self.location
        dest_x, dest_y = self.dest
        return loc_x, loc_y, dest_x, dest_y

    @beartype
    def moves_list(self) -> tuple[tuple]:
        """
        Return a list of possible moves.

        Returns:
            List[tuple]: List of possible moves.
        """
        return list(self.possible_moves.keys())

    @beartype
    def is_complete(self) -> bool:
        """
        Check if the flow is complete.

        Returns:
            bool: True if the flow is complete, False otherwise.
        """
        return self.location == self.dest

    @beartype
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
        current location. Also, update the previous location.
        """
        self.prev = self.location
        self.location = min(self.possible_moves, key=self.possible_moves.get)
