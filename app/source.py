
from photon import Photon
import numpy as np

class Source:


    def __init__(self, position, radius, normal):
        """Please make sure the normal vector is normalized :)"""
        self.position = position
        self.radius = radius
        self.normal = normal

    def drawRandomPhoton(self):
        """"Draws a random photon from the start of the beam"""

        # Pull the start time from a normal test pdf
        startTime = np.random.normal(5, 1, 1)[0]

        # TODO In the future find a vector perpendicular to the beam
        # normal and then rotate it randomly and scale it randomly
        # inside the beam radius to determine the start position
        radiusVector = np.array([0, 0, 0])
        initalPosition = self.position + radiusVector

        return Photon(initalPosition, self.normal, startTime)

