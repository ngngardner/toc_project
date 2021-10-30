"""Module for running traffic simluation."""

import numpy as np
import seaborn as sns
from beartype import beartype
from matplotlib import pyplot as plt

from traffic_sim.core.matrix.traffic import TrafficMatrix
from traffic_sim.core.sim.display import img_from_fig, save_gif
from traffic_sim.core.sim.history import TrafficHistory


class TrafficSim(object):
    """Class for running traffic simulation."""

    tm: TrafficMatrix
    history: TrafficHistory

    @beartype
    def __init__(self, matrix: TrafficMatrix) -> None:
        """Initialize traffic simulation.

        Args:
            matrix (TrafficMatrix): Traffic matrix to use for simulation.
        """
        self.tm = matrix

    @beartype
    def run(self, iterations: int) -> None:
        """Run the traffic simulation.

        Args:
            iterations (int): Number of iterations to run.
        """
        self.history = TrafficHistory()
        for _ in range(iterations):
            self.tm.step()
            self.history.append(flows=self.tm.flows, volume=self.tm.vmatrix)

    @beartype
    def savefig(self, path: str) -> None:
        """Save the simulation history to an animated .gif file.

        Args:
            path (str): Path to save the .gif file.
        """
        images = []
        for _, history in enumerate(self.history):
            # add heatmap to plot context (return value isn't used)
            plt.clf()
            sns.heatmap(
                history['volume'],
                cmap='YlGnBu',
                linewidth=0.5,
                vmin=0,
                vmax=np.max(self.tm.cmatrix),
            )
            im = img_from_fig()
            images.append(im)
        save_gif(images, path)
