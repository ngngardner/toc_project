"""Module for displaying simulation results."""

import io
from typing import List

from matplotlib import pyplot as plt
from PIL import Image


def img_from_fig() -> Image.Image:
    """
    Convert a Matplotlib figure to a PIL Image and return it.

    The figure is pulled from the current pyplot context, therefore the figure
    must be created and then drawn before calling this function.

    Returns:
        PIL Image array.
    """
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    return Image.open(buf)


def save_gif(
    images: List[Image.Image],
    path: str,
    duration: int = 750,
    loop: int = 0,
) -> None:
    """
    Given a list of images, create a gif and save to path as path.gif.

    Args:
        images (list): List of PIL images.
        path (str): Filename to save to.
        duration (int): Duration of each frame in milliseconds.
        loop (int): Number of times to loop the gif. 0 indicates infinite.
    """
    images[0].save(
        '{0}.gif'.format(path),
        append_images=images[1:],
        save_all=True,
        duration=duration,
        loop=loop,
    )
