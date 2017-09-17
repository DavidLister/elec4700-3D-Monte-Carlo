# geometry.py
#
# Started September 2017
#

import numpy as np

# Note, for multithreading to work, these classes must not change their state after init.

class Point:

    def __init__(self, x, y, z):
        self.array = np.array([x, y, z])

class Vector:

    def __init__(self, x, y, z):
        self.array = np.array([x, y, z])

class Ray:

    def __init__(self, start, end):
        self.start = start
        self.end = end

class Object:

    def __init__(self):
        self.priority = 0

    def contains(self, point):
        """Returns True/False if the point is inside the object"""
        pass

    def intersectsRay(self, ray):
        """Return True/False if the ray intercepts the object"""
        pass

    def getProperties(self):
        """Returns the properties object for inside the medium"""
        pass

    def getIntersection(self, ray):
        """Returns the intersection point and normal (if it exists)"""
        pass

