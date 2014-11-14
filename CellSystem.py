from dna import DNA
from cell import Cell, Herbivore
from stuff import Food
from vector import Vector

import random

class CellSystem(object):
    cells = []
    width = displayHeight
    height = displayHeight
    depth = displayHeight

    def __init__(self):
        pass

    ###################################
    def addCell(self, x, y):
        location = Vector([x, y])

        cell = Cell(location)
        cell.cs = self
        self.cells.append(cell)

    ## Ading cell at random position in cellsystem dimension
    def addRandomCell(self):
        location = Vector([random.randint(25, height - 25), random.randint(25, height-25), random.randint(25, height-25)])
        cell = Herbivore(l = location)
        cell.onDeath += self.onDeath
        cell.cs = self
        self.cells.append(cell)


    def onDeath(self, cell):
        if cell in self.cells:
            self.cells.pop(self.cells.index(cell))
        if cell in self.stuffList:
            self.stuffList.pop(self.stuffList.index(cell))

        cell = None

    def run(self):
        for cell in self.cells:
            cell.update()
            cell.display()

    def updateVisibleItems(self, creature):
        sightRange = creature.sightRange
        location = creature.location

        items = creature.visibleItems

        for stuff in self.stuffList:
            if stuff != creature:
                if stuff in items:
                    if location.dist(stuff.location) > sightRange / 2:
                        # stuff.detected = False
                        items.pop(items.index(stuff))
                    else:
                        pass
                        # stuff.detected = True
                else:
                    if location.dist(stuff.location) < sightRange / 2:
                        # stuff.detected = True
                        items.append(stuff)






