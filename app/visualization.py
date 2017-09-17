# visualization.py
#
# Started September 2017
#
# Used https://www.youtube.com/watch?v=Hqg4qePJV2U&t=827s as the starting point
#

# Controls:
# ESCAPE - Quit the app
# M - Toggle mouse capture

from pyglet.gl import *
from pyglet.window import key
import math
import random
import numpy as np
import geometry


scene = []

class Window (pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(320, 240)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.scene = get_scene()
        self.player = Player()

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 20000)
        self.Model()

    def push(self, pos, rot):
        # glPushMatrix()
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2], )

    def on_draw(self):
        self.clear()
        self.set3d()

        self.push(self.player.pos,self.player.rot)
        for object in self.scene:
            object.draw()

    def update(self, dt):
        self.player.update(dt, self.keys)

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self: self.lock, setLock)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()

        elif KEY == key.M:
            self.mouse_lock = not self.mouse_lock


class Player:

    def __init__(self):
        self.pos = [0, 0, 0]
        self.rot = [0, 0]

    def update(self, dt, keys):
        s = dt * 1000
        rotY = -self.rot[1]/180 * math.pi
        dx, dz = s*math.sin(rotY), s*math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx
            self.pos[2] -= dz
        if keys[key.A]:
            self.pos[0] -= dz
            self.pos[2] -= dx
        if keys[key.S]:
            self.pos[0] -= dx
            self.pos[2] += dz
        if keys[key.D]:
            self.pos[0] += dz
            self.pos[2] += dx
        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s

    def mouse_motion(self, dx, dy):
        SCALLER = 8
        dx/=SCALLER
        dy/=SCALLER
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0] > 90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90


class Model:

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

        colour = ("c3f", (0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1))
        x, y, z = 0, 0, -1
        X, Y, Z = x + 1, y + 1, z + 1

        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,z, x,y,Z, x,Y,Z, x,Y,z)), colour)
        self.batch.add(4, GL_QUADS, None, ("v3f", (X,y,Z, X,y,z, X,Y,z, X,Y,Z)), colour)
        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,z, X,y,z, X,y,Z, x,y,Z)), colour)
        self.batch.add(4, GL_QUADS, None, ("v3f", (x,Y,Z, X,Y,Z, X,Y,z, x,Y,z)), colour)
        self.batch.add(4, GL_QUADS, None, ("v3f", (X,y,z, x,y,z, x,Y,z, X,Y,z)), colour)
        self.batch.add(4, GL_QUADS, None, ("v3f", (x,y,Z, X,y,Z, X,Y,Z, x,Y,Z)), colour)

    def draw(self):
        self.batch.draw()


class Box:

    def __init__(self, cornerA, cornerB):
        self.cornerA = cornerA
        self.cornerB = cornerB
        self.batch=pyglet.graphics.Batch()

        base_colour = np.array((random.random(), random.random(), random.random()))
        x, y, z = cornerA.array
        X, Y, Z = cornerB.array

        self.batch.add(4, GL_QUADS, None, ("v3f", (x, y, z, x, y, Z, x, Y, Z, x, Y, z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))
        self.batch.add(4, GL_QUADS, None, ("v3f", (X, y, Z, X, y, z, X, Y, z, X, Y, Z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))
        self.batch.add(4, GL_QUADS, None, ("v3f", (x, y, z, X, y, z, X, y, Z, x, y, Z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))
        self.batch.add(4, GL_QUADS, None, ("v3f", (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))
        self.batch.add(4, GL_QUADS, None, ("v3f", (X, y, z, x, y, z, x, Y, z, X, Y, z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))
        self.batch.add(4, GL_QUADS, None, ("v3f", (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)), ("c3f", tuple(base_colour * (1 - random.random()/10)) * 4))

    def draw(self):
        self.batch.draw()

    def __str__(self):
        return "A:{}  B:{}".format(self.cornerA, self.cornerB)

def get_scene():
    return scene

def run():
    window = Window(width=600, height=400, caption="Visualization", resizable=True, vsync=True)
    glClearColor(0.5, 0.7, 1, 1)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)
    pyglet.app.run()

if __name__ == "__main__":
    import main
    # scene.append(Box(geometry.Point(0, 0, 0), geometry.Point(100, 100, 100)))
    # scene.append(Box(geometry.Point(110, 110, 110), geometry.Point(200, 200, 200)))
    # scene.append(Box(geometry.Point(10, 10, 10), geometry.Point(-100, -100, -100)))
    for obj in main.scene:
        if obj.visible:
            scene.append(obj.getModel())

    run()