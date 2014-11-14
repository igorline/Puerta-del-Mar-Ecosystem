import random

class DNA(object):
    genesLength = 5

    energy = {
        'name': 'energy',
        'min': 100,
        'max': 140
    }

    mass = {
        'name': 'mass',
        'min': 2.4,
        'max': 4.2
    }

    maxspeed = {
        'name': 'maxspeed',
        'min': 2.5,
        'max': 1.0
    }

    maxforce = {
        'name': 'maxforce',
        'min': 0.08,
        'max': 0.12
    }

    sightRange = {
        'name': 'sightRange',
        'min': 100,
        'max': 150
    }

    mapGenes = [energy, mass, maxspeed, maxforce, sightRange]

    def __init__(self):
        self.genes = []
        for x in xrange(len(self.mapGenes)):
            genVal = random.uniform(self.mapGenes[x]['min'], self.mapGenes[x]['max'])
            self.mapGenes[x]['real'] = genVal
            self.genes.append(genVal)

        for x in xrange(self.genesLength - len(self.mapGenes)):
            self.genes.append(random.random())
