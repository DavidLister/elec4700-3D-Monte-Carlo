# photon.py
#
# Basically just a data class for the photon, pretty anti-climactic

class Photon:
    def __init__(self, initialPosition, initalDirection):
        self.position = initialPosition
        self.direction = initalDirection
        self.time = 0

