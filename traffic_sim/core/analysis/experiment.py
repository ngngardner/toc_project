"""Module for running experimental results."""

from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
from beartype import beartype
from matplotlib import pyplot as plt

from traffic_sim.console import console
from traffic_sim.core.sim.history import TrafficHistory
from traffic_sim.matrix import TrafficMatrix, WeightedMatrix
from traffic_sim.sim import TrafficSim

base_path = Path.cwd() / 'output'
if not base_path.exists():
    base_path.mkdir(parents=True, exist_ok=True)


@beartype
def num_full_cells(cmatrix: np.ndarray, th: TrafficHistory) -> int:
    """Return the number of full cells in the history.

    Args:
        cmatrix: Capacity matrix to compare to.
        th (TrafficHistory): History to count full cells in.

    Returns:
        int: Number of full cells in the history.
    """
    counts = 0
    for vmatrix in th.volume_history:
        idxs = np.where(vmatrix > 0)
        counts += np.count_nonzero(cmatrix[idxs] == vmatrix[idxs])
    return counts


class TrafficExperiment(object):
    """Class for getting experimental results."""

    def __init__(
        self,
        experiments: int,
        trials: int,
        rows: int,
        cols: int,
        epochs: int,
    ) -> None:
        """Initialize the ExperimentRunner.

        Args:
            experiments: Number of experiments to run.
            trials: Number of trials per experiment.
            rows: Number of rows in the capacity matrix.
            cols: Number of columns in the capacity matrix.
            epochs: Number of epochs to run.
        """
        self.experiments = experiments
        self.trials = trials
        self.rows = rows
        self.cols = cols
        self.epochs = epochs
        self.res_df = pd.DataFrame(
            columns=[
                'density',
                'full_cells',
                'full_cells_w',
            ],
        )

    def run(self) -> None:
        """Run experiments."""
        for experiment in range(self.experiments):
            console.log('Experiment {0}'.format(experiment))
            for trial in range(self.trials):
                console.log('Trial {0}'.format(trial))
                density = trial / 100
                self.run_trial(density)

    @beartype
    def run_trial(self, density: float) -> None:
        """Run a single trial.

        Args:
            density: Density of the traffic matrix.
        """
        tm = TrafficMatrix(self.rows, self.cols, density=density)
        tm.cmatrix[:, 2] = 2
        tm.cmatrix[:, 8] = 2
        tm.cmatrix[3, :] = 3
        tm.cmatrix[:, 5] = 4

        wtm = WeightedMatrix(self.rows, self.cols, density=density)
        wtm.cmatrix = deepcopy(tm.cmatrix)
        wtm.set_weights()

        sim = TrafficSim(tm)
        sim.run(self.epochs)

        wsim = TrafficSim(wtm)
        wsim.run(self.epochs)

        num_full = num_full_cells(tm.cmatrix, sim.history)
        num_full_w = num_full_cells(wtm.cmatrix, wsim.history)

        self.res_df = self.res_df.append(
            {
                'density': density,
                'full_cells': num_full,
                'full_cells_w': num_full_w,
            },
            ignore_index=True,
        )
        console.log('Density: {0}'.format(density))
        console.log('Full cells: {0}'.format(num_full))
        console.log('Full cells (w): {0}'.format(num_full_w))

    def analyze(self) -> None:
        """Analyze the results."""
        # get average full cells per density
        avg_full_cells = self.res_df.groupby('density').mean()

        # save csv
        avg_full_cells.to_csv(base_path / 'avg_full_cells.csv')

        # save latex
        avg_full_cells.to_latex(base_path / 'avg_full_cells.tex')

        # create graph
        x1 = avg_full_cells.index.values
        y1 = avg_full_cells['full_cells'].values
        y2 = avg_full_cells['full_cells_w'].values

        plt.plot(x1, y1, label='Traffic')
        plt.plot(x1, y2, label='Weighted')
        plt.xlabel('Density')
        plt.ylabel('Number of full cells')
        plt.legend()
        plt.savefig(base_path / 'avg_full_cells.png')
