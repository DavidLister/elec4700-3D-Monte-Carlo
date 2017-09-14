# This is just rough dont judge me

import random

def move_and_scatter(particle, velocity):
    moveLength = random.uniform(0,1);
    particle[0] += velocity[0] * moveLength
    particle[1] += velocity[1] * moveLength
    particle[2] += velocity[2] * moveLength
    return random.uniform(-1, 1), random.uniform(-1,1), random.uniform(-1, 1)


if __name__ == '__main__':
    print('hello world')

    particle = [0, 0, 0]
    newVelocity = move_and_scatter(particle, (0, 1, 0))

    for i in range(10):
        print (particle)
        newVelocity = move_and_scatter(particle, newVelocity)


