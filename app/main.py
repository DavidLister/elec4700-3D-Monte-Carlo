# main.py
#
# Started September 2017
#

import geometry
import source
import numpy as np
import simulation
import threading
import time
import matplotlib.pyplot as plt

scene = []
scene.append(geometry.Box(geometry.Point(-5000, -2500, -5000), geometry.Point(5000, 2500, 5000), -1, geometry.LIGHT_FOG))
scene.append(geometry.Box(geometry.Point(-1000, -1000, -1500), geometry.Point(1000, 1000, -1600), 0, geometry.REFLECTOR, logging=True))
scene.append(geometry.Box(geometry.Point(-1000, -1000, 1500), geometry.Point(1000, 1000, 1600), 0, geometry.RECEIVER, logging=True))

sources = []
sources.append(source.Source(np.array([0, 0, 0]), np.array([1]), np.array([0, 0, 1])))

if __name__ == '__main__':
    print("Main")
    iterations = 10000
    threads = 8
    timeout = 30
    tracker = simulation.Tracker(scene, sources, iterations)
    pool = [threading.Thread(target=simulation.operator, args=(tracker, scene, timeout,)) for i in range(threads)]
    start = time.time()
    for op in pool:
        op.start()

    while sum([op.is_alive() for up in pool]) != 0:
        time.sleep(1)
    total = time.time() - start
    print("Total Time: ", total)
    print(iterations/1000/total, " thousand per second")

    tracker.plot()
    plt.show()

    print("Done!")
