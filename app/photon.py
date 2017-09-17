# photon.py
#
# Started September 2017
#
# Basically just a data class for the photon, pretty anti-climactic

import numpy as np

class Photon:
    def __init__(self, initialPosition, initalDirection, time):
        self.position = initialPosition
        self.direction = initalDirection
        self.time = time

    def __str__(self):
        return 'Position : ' + np.array_str(self.position) + ', Direction : ' + np.array_str(self.direction) + ', Time :' + str(self.time)