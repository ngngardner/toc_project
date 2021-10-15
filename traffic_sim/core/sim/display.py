"""Module for displaying simulation results."""

import io
from typing import List

import matplotlib.pyplot as plt

from PIL import Image

def img_from_fig(fig: plt.Figure) -> Image.Image:
    """
    Convert a Matplotlib figure to a PIL Image and return it.

    Args:
        fig: Matplotlib figure to convert.
    
    Returns:
        img: PIL Image array.
    """
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def save_gif(images: List[Image], filename: str) -> None:
    """
    Given a list of images, create a gif and save to filename.

    Args:
        images (list): List of PIL images.
        filename (str): Filename to save to.
    """
    images[0].save(
        filename,
        format='GIF',
        append_images=frames[1:],
        save_all=True,
        duration=100,
        loop=0
    )
