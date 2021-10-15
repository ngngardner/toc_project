"""Module for running traffic simluation."""

import matplotlib.pyplot as plt
import seaborn as sns

from traffic_sim.core.matrix.traffic import TrafficMatrix
from traffic_sim.core.sim.history import TrafficHistory
from traffic_sim.core.sim.display import img_from_fig, save_gif


class TrafficSim(object):
    """Class for running traffic simulation."""

    history: TrafficHistory
    tm: TrafficMatrix

    def __init__(self, matrix: TrafficMatrix) -> None:
        """Initialize traffic simulation.
        
        Args:
            matrix (TrafficMatrix): Traffic matrix to use for simulation.
        """
        self.tm = matrix

    def run(self, iterations: int) -> None:
        """Run the traffic simulation.

        Args:
            iterations (int): Number of iterations to run.
        """
        self.history = TrafficHistory()
        for _ in range(iterations):
            tm.step()
            self.history.append(flow=tm.flows, volume=tm.vmatrix)

    def savefig(self, path: str) -> None:
        """Save the simulation history to an animated .gif file.

        Args:
            path (str): Path to save the .gif file.
        """
        imList = []
        for i in range(len(self.history)):
            plt.clf()
            vmatrix = self.history.volume_history[i]
            fig = sns.heatmap(
                vmatrix,
                cmap="YlGnBu",
                linewidth=0.5,
                vmin=0,
                vmax=np.max(self.tm.cmatrix)
            )
            im = img_from_fig(fig)
            imList.append(im)
        save_gif(imList, path)
