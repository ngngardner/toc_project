"""Global console module."""

import logging

from rich.console import Console
from rich.logging import RichHandler


def init_console() -> Console:
    """Initialize console.

    Returns:
        Console: Console object.
    """
    return Console()


def init_logger():
    """Initialize logger."""
    logging.basicConfig(
        level=logging.getLevelName('INFO'),
        format='%(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()],
    )


init_logger()
console = init_console()
