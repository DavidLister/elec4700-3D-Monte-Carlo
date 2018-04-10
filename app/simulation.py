# simulation.py
#
# Started September 2017
#

import threading
import geometry
import random
import numpy as np
import matplotlib.pyplot as plt

class Event:

    def __init__(self, time):
        self.time = time

class Counter:

    def __init__(self, id):
        self.lock = threading.Lock()
        self.id = id
        self.events = []

    def addEvent(self, event):
        with self.lock:
            self.events.append(event)

    def plot(self):
        with self.lock:
            times = []
            for event in self.events:
                times.append(event.time)
            print(self.id, len(times))
            plt.hist(times, 500, normed=1, alpha=0.75)


class Tracker:

    def __init__(self, scene, sources, iterations):
        self.lock = threading.Lock()
        self.counters = {}
        self.sources = sources
        self.iterations = iterations

        for obj in scene:
            if obj.logging:
                self.counters[obj.getID()] = Counter(obj.getID())

        for obj in sources:
            self.counters[obj.getID()] = Counter(obj.getID())

    def addEvent(self, obj, event):
        with self.lock:
            # print(event.time)
            self.counters[obj.getID()].addEvent(event)

    def givePhoton(self):
        # todo make general
        with self.lock:
            if self.iterations > 0:
                print(self.iterations)
                self.iterations -= 1
                photon = self.sources[0].getPhoton()
            else:
                photon = None
        if photon is None:
            return photon
        self.addEvent(self.sources[0], Event(photon.time))
        return photon

    def plot(self):
        with self.lock:
            for key in self.counters.keys():
                self.counters[key].plot()



def get_cost(photon, scene):
    inside = [obj for obj in scene if obj.contains(photon.position)]
    max_p = inside[0].priority
    max_obj = inside[0]
    for obj in inside:
        if obj.priority > max_p:
            max_obj = obj
            max_p = obj.priority
    mfp = max_obj.properties.meanFreePath
    cost = random.gauss(mfp, mfp * 0.25) #TODO make 2 a property
    cost = abs(cost)
    return cost

def get_path(photon, scenem, cost):
    d = cost / np.linalg.norm(photon.direction) # Using default cost 1/mm #Todo add pelrin local deviation
    return geometry.Ray(photon.position, photon.position + photon.direction * d)

def intersection(ray, scene):
    for obj in scene:
        if obj.intersectsRay(ray):
            return True
    return False

def change_medium(ray, scene, photon):
    object = []
    point = []
    dist = []
    for obj in scene:
        if obj.intersectsRay(ray):
            pt = obj.intersect(ray)
            object.append(obj)
            point.append(pt)
            dist.append(np.linalg.norm(pt - photon.position))
    target = object[dist.index(min(dist))]
    point = point[dist.index(min(dist))]
    path = point - photon.position
    dist = np.linalg.norm(path)
    uvect = path/dist
    print(target, path, point, dist, uvect)

    if random.random()  <= target.properties.absorbance:
        print("absorbed!")
        photon.absorbed = True

    elif random.random() <= target.properties.reflectance:
        point = point - uvect
        print("Reflect!", point, uvect)
        reflect(photon, 1*uvect)

    else:
        point = point + uvect
        refract(photon, None, None) # Todo

    move(photon, point, 1)

    if target.logging:
        return target
    return None


def move(photon, point, n=1):
    dist = np.linalg.norm(point - photon.position)
    photon.addDistance(dist, n)
    photon.position = point

def reflect(photon, normal):
    # Todo, make this reasonable
    normal = normal
    #dir = np.array([random.random(), random.random(), random.random()])
    #dir = dir / np.linalg.norm(dir)
    photon.direction = normal

def refract(photon, old, new):
    # Todo, make this reasonable
    dir = np.array([random.random(), random.random(), random.random()])
    dir = dir / np.linalg.norm(dir)
    photon.direction = dir

def scatter(photon, scene):
    # Todo, make this reasonable
    dir = np.array([random.random(), random.random(), random.random()])
    dir = dir / np.linalg.norm(dir)
    photon.direction = dir

def is_over(photon, scene, timeout):
    if photon.absorbed:
        return True
    elif photon.time >= timeout:
        return True
    # todo, fix this
    inside = [obj for obj in scene if obj.contains(photon.position)]
    if len(inside) == 0:
        return True

    return False


def operator(Tracker, scene, timeout):
    # todo, make this way faster and less rundudant

    done = False
    while not done:
        photon = Tracker.givePhoton()
        if photon is not None:
            over = False
            while not over:
                cost = get_cost(photon, scene)
                ray = get_path(photon, scene, cost)
                if intersection(ray, scene):
                    log = change_medium(ray, scene, photon)
                    if log is not None:
                        Tracker.addEvent(log, Event(photon.time))
                else:
                    move(photon, ray.end)
                    scatter(photon, scene)
                over = is_over(photon, scene, timeout)
        else:
            done = True
