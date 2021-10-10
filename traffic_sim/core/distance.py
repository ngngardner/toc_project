"""Distance module for core functions."""

from typing import List, Tuple


def coord_list(coords: tuple) -> List[Tuple[int, int]]:
    """Convert a tuple of coordinates to a list of coordinates.

    Useful for converting the output of np.where to a list of coordinates.

    Args:
        coords(tuple): Tuple of coordinates.

    Returns:
        List of coordinates.
    """
    return [(coord[0], coord[1]) for coord in coords]


def euclidean(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate the distance between two points.

    Args:
        p1: First point.
        p2: Second point.

    Returns:
        The distance between the two points.
    """
    diff_x = p1[0] - p2[0]
    diff_y = p1[1] - p2[1]
    return (diff_x ** 2 + diff_y ** 2) ** 0.5
