# geometry.py
#
# Started September 2017
#

import numpy as np
import visualization
import random

# Note, for multithreading to work, these classes must not change their state after init.

def in_range(val, lst):
    """Returns True if the values is in the range of lst where lst is assumed to be sorted from smallest to biggest"""
    if len(lst) == 2:
        return val>lst[0] and val < lst[1]
    elif len(lst) == 1:
        return True
    return False

class Point:

    def __init__(self, x, y, z):
        self.array = np.array([x, y, z])

    def getX(self):
        return self.array[0]

    def getY(self):
        return self.array[1]

    def getZ(self):
        return self.array[2]

    def __str__(self):
        return str("{}, {}, {}").format(self.array[0], self.array[1], self.array[2])


class Ray:

    def __init__(self, start, end):
        """Expects a np array for start and end"""
        self.start = start
        self.end = end
        delta = end - start
        self.vector = delta


class Object:

    def __init__(self, priority, properties, visible = False, logging=False):
        self.priority = priority
        self.logging = logging
        self.properties = properties
        self.visible = visible
        self.id = hash(random.random())

    def contains(self, point):
        pass

    def intersectsRay(self, ray):
        """Return True/False if the ray intercepts the object"""
        pass

    def getProperties(self):
        """Returns the properties object for inside the medium"""
        return self.properties

    def getIntersection(self, ray):
        """Returns the intersection point and normal (if it exists)"""
        pass

    def getModel(self):
        pass

    def getID(self):
        return self.id

class Box(Object):

    def __init__(self, corner1, corner2, priority, properties, visible=True, logging = False):
        super(Box, self).__init__(priority, properties, visible, logging)
        self.cornerA = corner1
        self.cornerB = corner2
        self.xrange = [self.cornerA.getX(), self.cornerB.getX()]
        self.xrange.sort()
        self.yrange = [self.cornerA.getY(), self.cornerB.getY()]
        self.yrange.sort()
        self.zrange = [self.cornerA.getZ(), self.cornerB.getZ()]
        self.zrange.sort()

        x, y, z = self.cornerA.array
        X, Y, Z = self.cornerB.array
        self.points = []
        self.points.append(np.array([X, y, z]))
        self.points.append(np.array([X, Y, z]))
        self.points.append(np.array([x, Y, z]))
        self.points.append(np.array([x, Y, z]))
        self.points.append(np.array([x, y, Z]))
        self.points.append(np.array([x, y, Z]))
        self.points.append(np.array([X, y, Z]))
        self.points.append(np.array([X, Y, Z]))

        self.planes = []
        self.planes.append(Plane(self.points[0], self.points[3], self.points[4]))
        self.planes.append(Plane(self.points[1], self.points[2], self.points[7]))
        self.planes.append(Plane(self.points[5], self.points[0], self.points[1]))
        self.planes.append(Plane(self.points[2], self.points[3], self.points[4]))
        self.planes.append(Plane(self.points[0], self.points[1], self.points[2]))
        self.planes.append(Plane(self.points[4], self.points[5], self.points[6]))

    def contains(self, point):
        """Returns True/False if the point is inside the object"""
        if in_range(point[0], self.xrange) and in_range(point[0], self.yrange) and in_range(point[0], self.zrange):
            return True
        return False

    def intersectsRay(self, ray):
        for plane in self.planes:
            if plane.intersectsRay(ray):
                return True
        return False

    def intersect(self, ray):
        dist = []
        point = []
        for plane in self.planes:
            if plane.intersectsRay(ray):
                pt = plane.intersect(ray)
                dist.append(np.linalg.norm(pt - ray.start))
                point.append(pt)
        if len(dist) > 0:
            return point[dist.index(min(dist))]
        return None

    def getModel(self):
        return visualization.Box(self.cornerA, self.cornerB)

    def __str__(self):
        return "A:{}  B:{}".format(self.cornerA, self.cornerB)

    def getID(self):
        return self.__str__()


class Plane:

    def __init__(self, a, b, c):
        """Creates a plane from 3 points, expects the points as a np arrays
            For intersertion detection, it assumes plane is normal to one of x, y or z axis"""
        self.normal = np.cross(a - b, c - b)
        self.offset = np.sum(b * self.normal)
        self.xbounds = sorted(list(set([a[0], b[0], c[0]])))
        self.ybounds = sorted(list(set([a[1], b[1], c[1]])))
        self.zbounds = sorted(list(set([a[2], b[2], c[2]])))


    def intersectsRay(self, ray):
        # Check to see if the vector even points towards the plane
        if np.dot(self.normal, ray.vector) >= 0:
            return False

        else:
            d = (self.offset - np.dot(ray.start, self.normal))/np.dot(ray.vector, self.normal)
            intercept = d * ray.vector + ray.start
            if in_range(intercept[0], self.xbounds) and in_range(intercept[1], self.ybounds) and in_range(intercept[2], self.zbounds):
                if np.linalg.norm(ray.vector) > np.linalg.norm(intercept - ray.start) and np.linalg.norm(intercept - ray.start) > 0.1:
                    return True
                return False
            return False

    def intersect(self, ray):
        d = (self.offset - np.dot(ray.start, self.normal)) / np.dot(ray.vector, self.normal)
        intercept = d * ray.vector + ray.start
        return intercept



class OpticalProperties:

    def __init__(self, n, mean_free_path, absorbance, reflectance, counter=False):
        self.n = n
        self.meanFreePath = mean_free_path # mm
        self.absorbance = absorbance
        self.reflectance = reflectance
        self.counter = counter

AIR = OpticalProperties(1.00029, 10 * 10 ** 6, 0, 0)
LIGHT_FOG = OpticalProperties(1.00029, 2500, 0, 0)
FOG_SIMPLE = OpticalProperties(1.00029, 50, 0, 0)
REFLECTOR = OpticalProperties(1, 1, 0, 1)
PARTIAL = OpticalProperties(1, 10, 0.33, 0.33)
RECEIVER = OpticalProperties(1, 1, 1, 0, counter=True)

if __name__ == "__main__":
    p = Plane(np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([1, 1, 0]))
    r = Ray(np.array([0, 0, -2]), np.array([0, 0, 2])) #todo fix this bug (0, 0, 0)
    b = Box(Point(-1, -1, -1), Point(1, 1, 1), 1, AIR)
    print(b.contains(np.array([0, 0, 0])))
    print(p.intersect(r))
    print(b.intersect(r))