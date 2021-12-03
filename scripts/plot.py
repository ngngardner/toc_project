"""Create plot from avg_full_cells.csv"""

from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# load from file
base_path = Path.cwd() / 'output'
path = base_path / 'avg_full_cells.csv'
avg_full_cells = pd.read_csv(path)


# create graph
x1 = avg_full_cells.index.values / 100
y1 = avg_full_cells['full_cells'].values
y2 = avg_full_cells['full_cells_w'].values

sns.set_style('whitegrid')
sns.set_context('paper')
sns.set_palette('hls')

plt.plot(x1, y1, label='Non-weighted')
plt.plot(x1, y2, label='Weighted')
plt.xlabel('Density')
plt.ylabel('Average Traffic Jams')
plt.title('Weighted vs. Non-weighted Average Simulated Traffic Jams')
plt.legend()
plt.savefig(base_path / 'avg_full_cells.png')
