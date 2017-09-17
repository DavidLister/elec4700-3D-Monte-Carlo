# main.py
#
# Started September 2017
#

import geometry
import visualization


scene = []
scene.append(geometry.Box(geometry.Point(-5000, -2500, -5000), geometry.Point(5000, 2500, 5000), -1, geometry.AIR))
scene.append(geometry.Box(geometry.Point(-50, -50, -4600), geometry.Point(50, 50, -4500), 0, geometry.RECEIVER))
scene.append(geometry.Box(geometry.Point(-50, -50, 4500), geometry.Point(50, 50, 4600), 0, geometry.RECEIVER))

if __name__ == '__main__':
    print("Main")
    pass

