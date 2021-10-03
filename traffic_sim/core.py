"""Core functions for traffic_sim."""

import logging

logger = logging.getLogger(__name__)


def example(pstr: str) -> str:
    """Log input string as a example package function, and returns it.

    Args:
        pstr (str): String to be logged.

    Returns:
        str: Input string.
    """
    logger.info(pstr)
    return pstr
