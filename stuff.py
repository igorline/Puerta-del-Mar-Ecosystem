from __future__ import division
import random
import time

from vector import Vector
from utils import EventHook

resolution = 2
margin = 60
season = 0

class Stuff(object):

    def __init__(self, x, y):
        self.location = Vector([x, y])
        self.mass = 2
        self.size = self.mass * resolution

        self.detected = False

    def display(self):
        noStroke()
        if self.detected:
            fill(255, 0, 0)
        ellipse(self.location.x, self.location.y, self.size, self.size)


class Food(Stuff):
    season = 0
    def __init__(self, x, y):
        super(Food, self).__init__(x, y)
        self.type = 'food'
        self.isOff = False
        self.mass = 1
        self.size = self.mass * resolution
        self.growthCycle = 20
        self.startTime = time.time()


    def run(self):
        self.update()
        self.display()

    def update(self):
        currentTime = time.time()
        if currentTime - self.startTime > self.growthCycle:
            self.mass += 1
            self.size = self.mass * resolution
            self.startTime = currentTime

        if self.mass > 1:
            self.isOff = False

    def display(self):
        if self.isOff:
            fill(100, 50, 0)
        else:
            fill(50, 255, 50)

        super(Food, self).display()

    def eat(self):
        self.mass -= 1
        if self.mass <= 1:
            self.mass = 1
            self.isOff = True
            self.startTime = time.time()

        self.size = self.mass * resolution



