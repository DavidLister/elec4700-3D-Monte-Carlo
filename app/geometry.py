# geometry.py
#
# Started September 2017
#

import numpy as np

# Note, for multithreading to work, these classes must not change their state after init.

def in_range(val, lst):
    """Returns True if the values is in the range of lst where lst is assumed to be sorted from smallest to biggest"""
    return val>lst[0] and val < lst[1]

class Point:

    def __init__(self, x, y, z):
        self.array = np.array([x, y, z])

    def getX(self):
        return self.array[0]

    def getY(self):
        return self.array[1]

    def getZ(self):
        return self.array[2]


class Vector:

    def __init__(self, x, y, z):
        self.array = np.array([x, y, z])


class Ray:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        delta = end.array - start.array
        self.vector = Vector(delta[0], delta[1], delta[2])


class Object:

    def __init__(self, priority, properties, logging=False):
        self.priority = priority
        self.logging = logging
        self.properties = properties

    def contains(self, point):
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

def Box(Object):

    def __init__(self, corner1, corner2, priority, properties, logging = False):
        super(Box, self).__init__(priority, properties, logging)
        self.cornerA = corner1
        self.cornerB = corner2
        self.xrange = [self.cornerA.getX(), self.cornerB.getX()]
        self.xrange.sort()
        self.yrange = [self.cornerA.getY(), self.cornerB.getY()]
        self.yrange.sort()
        self.zrange = [self.cornerA.getZ(), self.cornerB.getZ()]
        self.zrange.sort()

    def contains(point):
        """Returns True/False if the point is inside the object"""
        if not in_range(point.getX(), self.xrange):
            return False
        elif not in_range(point.getY(), self.yrange):
            return False
        elif not in in_range(point.getZ(), self.zrange):
            return False
        else:
            return True



class OpticalProperties:

    def __init__(self, n, mean_free_path):
        self.n = n
        self.meanFreePath = mean_free_path # mm

AIR = OpticalProperties(1.00029, 10 * 10 ** 6)
FOG_SIMPLE = OpticalProperties(1.00029, 50)