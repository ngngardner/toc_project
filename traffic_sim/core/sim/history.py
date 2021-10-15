"""Module to store and retrieve simulation history."""

from typing import List

import numpy as np

from traffic_sim.core.flow.flow import TrafficFlow


class TrafficHistory(object):
    """Traffic history class to store and retrieve simulation history."""

    flow_history: List[List[TrafficFlow]]
    volume_history: List[np.ndarray]

    def __init__(self):
        """Initialize history class."""
        self.clear()

    def __iter__(self):
        """Iterate over history.

        Yields:
            TrafficFlow: Traffic flow object.
        """
        yield from (
            {
                'flows': flow,
                'volume': volume,
            }
            for flow, volume in zip(self.flow_history, self.volume_history)
        )

    def clear(self):
        """Clear history."""
        self.flow_history = []
        self.volume_history = []

    def append(self, flows: List[TrafficFlow], volume: np.ndarray):
        """Append flow and volume to history.

        Args:
            flows (List[TrafficFlow]): List of traffic flows.
            volume (np.ndarray): Traffic volume matrix.
        """
        self.flow_history.append(flows)
        self.volume_history.append(volume)
