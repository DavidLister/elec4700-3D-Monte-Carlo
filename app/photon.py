# photon.py
#
# Started September 2017
#
# Basically just a data class for the photon, pretty anti-climactic

import numpy as np

C = 299792458 # m/s
C = C * 1000 / (10 ** 9) # Conversion from m to mm and s to ns for the base units

class Photon:
    def __init__(self, initialPosition, initalDirection, time):
        self.position = initialPosition
        self.direction = initalDirection
        self.time = time # 1 unit is 1 ns, not one second
        self.absorbed = False

    def addDistance(self, dist, n=1):
        self.time += dist * n / C

    def __str__(self):
        return 'Position : ' + np.array_str(self.position) + ', Direction : ' + np.array_str(self.direction) + ', Time :' + str(self.time)