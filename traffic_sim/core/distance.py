"""Distance module for core functions."""

from beartype import beartype


@beartype
def coord_list(coords: tuple) -> list[tuple[int, int]]:
    """Convert a tuple of coordinates to a list of coordinates.

    Useful for converting the output of np.where to a list of coordinates.

    Args:
        coords(tuple): Tuple of coordinates.

    Returns:
        List of coordinates.
    """
    res = []
    size = range(len(coords[0]))
    for idx in size:
        x_coord = int(coords[0][idx])
        y_coord = int(coords[1][idx])
        res.append((x_coord, y_coord))
    return res


def euclidean(p1: tuple[int, int], p2: tuple[int, int]) -> int:
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
