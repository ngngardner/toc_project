"""Module to store and retrieve simulation history."""

from typing import List

import numpy as np

from traffic_sim.core.flow import TrafficFlow

class TrafficHistory:
    """Traffic history class to store and retrieve simulation history."""

    flow_history = List[List[TrafficFlow]]
    volume_history = List[np.ndarray]

    def __init__(self):
        """Initialize history class."""
        self.clear()

    def __len__(self):
        """Return length of history.
        
        Both histories should be the same length.
        """
        return len(self.flow_history)

    def clear(self):
        """Clear history."""
        self.flow_history = []
        self.volume_history = []

    def append(self, flows: List[TrafficFlow], volume: np.ndarray):
        """Append flow and volume to history."""
        self.flow_history.append(flows)
        self.volume_history.append(volume)
