from __future__ import division
import random
from vector import Vector
from utils import translatemap, clamp, EventHook
from dna import DNA
from stuff import Food
import time

margin = 25
width = displayHeight
energyFood = 80
depth = displayHeight


states = {
        'detect': 'detect',
        'decide': 'decide',
        'eat': 'eat',
        'escape': 'escape',
        'attack': 'attack',
        'copulate': 'copulate'
}

class Thing(object):
    def __init__(self, *args, **kwargs):
        super(Thing, self).__init__(*args, **kwargs)
        location = kwargs.get('l', None)
        x, y, z = location.x, location.y, location.z
        self.location = Vector([x, y, z])
        self.mass = 1
        self.resolution = 3
        self.size = self.mass * self.resolution

        self.detected = False
        self.isOff = False
        
    def display(self):
        noStroke()
        if self.detected:
            fill(255, 0, 0)
        #ellipse(self.location.x, self.location.y, self.size, self.size)
        sphere(self.size) 

class Plant(Thing):
    def __init__(self, x, y, z):
        self.type = 'food'
        self.growthCycle = 20
        self.startTime = time.time()

        l = Vector([x, y, z])

        super(Plant, self).__init__(l=l)

    def run(self):
        self.update()
        self.display()

    def update(self):
        currentTime = time.time()
        if currentTime - self.startTime > self.growthCycle:
            self.mass += 1
            self.size = self.mass * self.resolution
            self.startTime = currentTime

        if self.mass > 1:
            self.isOff = False

    def display(self):
        if self.isOff:
            fill(100, 50, 0)
        else:
            fill(50, 255, 50)

        fill(167, 212, 27)

        pushMatrix()
        translate(self.location.x, self.location.y, self.location.z)
        super(Plant, self).display()
        popMatrix()

    def eat(self):
        self.mass -= 1
        if self.mass <= 1:
            self.mass = 1
            self.isOff = True
            self.startTime = time.time()

        self.size = self.mass * self.resolution


class Alive(object):
    
    def __init__(self, *args, **kwargs):
        self.wandertheta = 0
        self.wanderphi = 0
        self.wanderpsi = 0
        
    def applyForce(self, force):
        # We could add mass here if we want A = F / M
        self.acceleration = self.acceleration.add(force)

    def update(self):
        self.velocity = self.velocity.add(self.acceleration).limit(self.maxspeed)
        self.location = self.location.add(self.velocity)
        self.accelertion = Vector([0, 0])
        self.boundaries()

    ####################################
    #
    # Alignment
    # For every nearby boid in the system, calculate the average velocity
    #
    # (c) Dan Shiffman
    # https://github.com/shiffman/The-Nature-of-Code-Examples/blob/master/chp6_agents/flocking_sliders/Boid.pde#L143
    #
    ####################################
    def align (self, boids):
        neighbordist = 50
        steer = Vector([0, 0])
        count = 0
        for other in boids:
            d = self.location.dist(other.location)
            if d > 0 and d < neighbordist:
                steer = steer.add(other.velocity)
                count += 1
        if count > 0:
            steer = steer.div(count)
            # Implement Reynolds: Steering = Desired - Velocity
            steer = steer.normalize().mult(self.maxspeed).sub(self.velocity).limit(self.maxforce)

        return steer

    ####################################
    #
    # Cohesion
    # For the average location (i.e. center) of all nearby boids, calculate steering vector towards that location
    #
    # (c) Dan Shiffman
    # https://github.com/shiffman/The-Nature-of-Code-Examples/blob/master/chp6_agents/flocking_sliders/Boid.pde#L167
    #
    ####################################
    def cohesion (self, boids):
        neighbordist = 50 
        sum = Vector([0, 0]) # Start with empty vector to accumulate all locations
        count = 0
        for other in boids:
            d = self.location.dist(other.location)
            if d > 0 and d < neighbordist:
                sum = sum.add(other.location) # Add location
                count += 1


        if count > 0:
            sum = sum.div(count)
            # TODO: Rewrite this
            desired = sum.sub(self.location).normalize().mult(self.maxspeed)

            # Steering
            desired = desired.sub(self.velocity).limit(self.maxforce)
            return desired

            #return self.seek(sum)

        return sum

    
    ####################################
    #
    # Separation
    # Method checks for nearby boids and steers away
    #
    # (c) Dan Shiffman
    # https://github.com/shiffman/The-Nature-of-Code-Examples/blob/master/chp6_agents/flocking_sliders/Boid.pde#L112
    #
    ####################################
    def separate(self, boids):
        desiredseparation = 25
        steer = Vector([0, 0])
        count = 0

        # For every boid in the system, check if it's too close
        for other in boids:
            d = self.location.dist(other.location)

            # If the distance is greater than 0 and less than an arbitrary amount (0 when you are yourself)
            if d > 0 and d < desiredseparation:
                # Calculate vector pointing away from neighbor
                diff = self.location.sub(other.location)
                diff = diff.normalize().div(d) # Weight by distance
                steer = steer.add(diff);
                count += 1 # Keep track of how many
        # Average -- divide by how many
        if count > 0:
            steer = steer.div(count)

            # Implement Reynolds: Steering = Desired - Velocity
            steer = steer.normalize().mult(self.maxspeed).sub(self.velocity).limit(self.maxforce)

        return steer
    
  


    ###################################
    #
    # Wandering
    # 
    # (c) Daniel Shiffman
    # https://github.com/shiffman/The-Nature-of-Code-Examples/blob/master/chp6_agents/Exercise_6_04_Wander/Vehicle.pde#L44
    #
    ###################################
    def wander(self):
        # TODO: Read
        wanderR = 25      # Radius for our "wander circle"
        wanderD = 80      # Distance for our "wander circle"
        change = 0.3
        self.wandertheta += -change + random.random() * 2 * change       
        self.wanderphi += -change + random.random() * 2 * change       
        self.wanderpsi += -change + random.random() * 2 * change       
        # Randomly change wander theta

        # Now we have to calculate the new location to steer towards on the wander circle
        circleloc = self.velocity.normalize().mult(wanderD).add(self.location) 
        # Start with velocity
        # Normalize to get heading
        # Multiply by distance
        # Make it relative to boid's location

        h = self.velocity.heading      # We need to know the heading to offset wandertheta

        circleOffset = Vector([wanderR*cos(self.wandertheta+h), wanderR*sin(self.wanderphi+h), wanderR*sin(self.wanderpsi+h)])
        target = circleloc.add(circleOffset)

        self.seek(target)

    #####################################
    #
    # A method that calculates and applies a steering force towards a target
    # STEER = DESIRED MINUS VELOCITY
    # 
    # (c) Daniel Shiffman
    # https://github.com/shiffman/The-Nature-of-Code-Examples/blob/master/chp6_agents/Exercise_6_04_Wander/Vehicle.pde#L74
    #
    #####################################
    def seek(self, target):
        # A vector pointing from the location to the target
        desired = target.sub(self.location)

        # Normalize desired and scale to maximum speed
        desired = desired.normalize().mult(self.maxspeed)

        # Steering = Desired minus Velocity
        steer = desired.sub(self.velocity)
        # Limit to maximum steering force
        steer = steer.limit(self.maxforce)

        self.applyForce(steer)


    def boundaries(self):
        desired = None

        #TODO: Rewrite 
        if (self.location.x < margin):
            desired = Vector([self.maxspeed, self.velocity.y, self.velocity.z])
        elif self.location.x > height - margin:
            desired = Vector([-self.maxspeed, self.velocity.y, self.velocity.z])

        if (self.location.y < margin):
            desired = Vector([self.velocity.x, self.maxspeed, self.velocity.z])
        elif self.location.y > height - margin:
            desired = Vector([self.velocity.x, -self.maxspeed, self.velocity.z])

        if (self.location.z < margin):
            desired = Vector([self.velocity.x, self.velocity.y, self.maxspeed])
        elif self.location.z > height - margin:
            desired = Vector([self.velocity.x, self.velocity.y, -self.maxspeed])
            

        if desired: 
            desired = desired.normalize().mult(self.maxspeed).sub(self.velocity).limit(self.maxforce)
            self.applyForce(desired)
        

# Living creature
class Cell(Thing, Alive):
    def __init__(self, *args, **kwargs):
        self.maxspeed = 4.5
        self.health = 130
        self.energy = 0
        self.energyWaste = 0.05
        self.maxforce = 0.06
        self.sightRange = 50

        self.isDead = False
        self.countdown = 0
        self.target = None
        self.learningRate = 5
        self.counter = 0
        self.locked = False
        self.hitted = True

        self.visibleItems = []

        self.r = 6

        self.couple = None

        self.acceleration = Vector([0, 0, 0])
        self.velocity = Vector([0, 0, 0])

        self.onDeath = EventHook()

        super(Cell, self).__init__(*args, **kwargs)

    def update(self):
        if self.health <= 0:
            self.onDeath.fire(self)

        super(Cell, self).update()


        
class Herbivore(Cell):

    def __init__(self, *args, **kwargs):

        k = kwargs
        self.location = kwargs.get('l', None)
        dna = kwargs.get('dna', None)
    
        super(Herbivore, self).__init__(l=self.location, dna=dna)

        # Adding hooks
        self.onBirth = EventHook()
        self.locked = False
        self.type = "herbivore"

        # DNA stuff
        if kwargs.get('dna', None):
            self.dna = dna
        else:
            self.dna = DNA()

        self.energy = self.dna.energy['real']
        self.mass = self.dna.mass['real']
        self.maxspeed = self.dna.maxspeed['real']
        self.maxforce = self.dna.maxforce['real']
        self.sightRange = self.dna.sightRange['real']

        self.state = states['detect']


    ##############################
    def run(self):
        self.update()
        self.display()

    def update(self):

        # Updating velocity and acceleration depending on action
        self.detect(self.cs.stuffList)
        if not self.locked:
            if self.state == states['detect']:
                self.move(self.cs.cells)
            elif self.state == states['eat']:
                self.eat(self.target)
            elif self.state == states['escape']:
                self.escape(self.target)
        else:
            self.acceleration = Vector([0, 0, 0])
            self.velocity = Vector([0, 0, 0])

        super(Herbivore, self).update()


    def display(self):
        health = translatemap(self.health, 0, 130, 0, 255)

        fill(255, 0, 0, health)

        # ellipse(self.location.x, self.location.y, self.size, self.size)
        pushMatrix()
        translate(self.location.x, self.location.y, self.location.z)
        sphere(self.size)
        # rotate(self.velocity.x, self.velocity.y, self.velocity.z)
        # 
        # rotateX(self.acceleration.x)
        # rotateY(self.acceleration.y)
        # rotateZ(self.acceleration.z)
        # box(self.size, 20, 20)
        popMatrix()
        noStroke()



        #fill(255, 0, 0, 10)
        #pushMatrix()
        #translate(self.location.x, self.location.y, self.location.z)
        # sphere(self.sightRange)
        # ellipse(self.location.x, self.location.y, self.sightRange, self.sightRange)
        #popMatrix()

        stroke(200, 200, 200, health)
        if self.state == states['eat']:
            stroke(0, 255, 0, health)
        if self.state == states['escape']:
            stroke(255, 0, 0, health)
        if self.state == states['attack']:
            stroke(255, 255, 0, health)
        elif self.state == states['copulate']:
            stroke(247, 170, 170, health)

        fill(0, 127, 255, health)
        fill(0, 0, 145, health)
        
        noStroke()
        
        if self.detected:
            fill(255, 0, 0, 100)

        fill(96, 211, 200, health)

        # ellipse(self.location.x, self.location.y, self.size, self.size)
        pushMatrix()
        translate(self.location.x, self.location.y, self.location.z)
        sphere(self.size)
        popMatrix()
        noStroke()



    #################################
    def move(self, cells):
        self.wander()
        # flock = self.flock(cells)

        # Arbitrary weights for these forces
        # wand = wand.mult(i).limit(self.maxforce)
        #flock = flock.mult(g).limit(self.maxforce)

        # self.applyForce(wand)
        # self.applyForce(flock)

    ##################################
    # FIXME: General Method
    def flock(self, cells):
        sep = self.separate(cells)
        ali = self.align(cells)
        coh = self.cohesion(cells)

        sep = sep.mult(1.5)
        ali = ali.mult(1.0)
        coh = coh.mult(1.0)

        flock = Vector([0, 0])
        flock.add(sep).add(ali).add(coh)

        return flock

    #################################
    def detect(self, stuffList):
        self.cs.updateVisibleItems(self)
        closestDist = 10000
        closest = None

        for stuff in self.visibleItems:
            if stuff.type == 'carnivore':
                self.state = states['escape']
                self.target = stuff
                return

        for stuff in self.visibleItems:
            dist = stuff.location.dist(self.location)
            if dist < closestDist:
                closestDist = dist
                closest = stuff

        if closest:
            self.target = closest
            self.state = states['eat']
        else:
            self.state = states['detect']


    def eat(self, stuff):
        if not stuff.isOff:
            self.state = states['eat']

            desired = stuff.location.sub(self.location)
            d = desired.magSq()

            if stuff.type == 'food':
                # Speed to eat food
                m = translatemap(d, 0, 10000, 0.25, self.maxspeed)
                desired = desired.setMag(m)

                # Calculate the steering force in the desired Vector
                desired = desired.sub(self.velocity).limit(self.maxforce)
                self.applyForce(desired)
                # self.energy += 10

                # If close enough eat
                if (d - stuff.size < self.size * self.size / 4.0):
                    stuff.eat()

                    # self.evaluate()
                    self.state = states['detect']
                    #self.objetivo = None
                    #self.tipoAccion = ""

        else:
            self.state = states['detect']
            #self.objetivo = None
            #self.tipoAccion = ""


    ###################################
    def escape(self, stuff):
        if hasattr(stuff, 'isDead') and not stuff.isDead:
            self.state = states['escape']
            desired = stuff.location.sub(self.location)
            d = desired.magSq()
            desired = desired.mult(-1).sub(self.velocity).limit(self.maxforce)

            if (d < self.sightRange*self.sightRange + 1):
                self.applyForce(desired)
            else:
                self.evaluate()
                self.state = states['detect'] 
                self.target = None

        else:
            self.state = states['detect']
            #self.objetivo = None
            #self.tipoAccion = ""



    ####################################
    def deathManWalking(self):
        self.maxforce = 0
        if self.countdown >= 255:
            self.isDead = True
            self.onDeath.fire(self)
        else:
            self.countdown += 1



class Carnivore(Cell):
    def __init__(self, x, y):
        self.location = Vector([x, y])
        super(Carnivore, self).__init__(self.location)
        self.type = 'carnivore'

        self.mass = 2 
        self.size = self.mass * self.resolution

        self.sightRange = 500

    
    def __init__(self, x, y, z):
        self.location = Vector([x, y, z])
        super(Carnivore, self).__init__(l=self.location)
        self.type = 'carnivore'

        self.mass = 2
        self.size = self.mass * self.resolution

        self.sightRange = 500

    def run(self):
        if self.target == None:
            self.detect(self.cs.cells)
        else:
            self.wander()
            if self.target.isDead:
                self.target = None

        self.update()
        self.display()


    ################################
    # FIXME: Common update?
    def update(self):
        self.detect(self.cs.cells)
        if self.target:
            removeTarget = False
            self.seek(self.target.location)
            if self.target.location.dist(self.location) < self.size / 2:
                if not self.target.hitted:
                    self.target.health -= 60
                    removeTarget = True

                self.target.hitted = True
            else:
                self.target.hitted = False

            
            if self.target.health <= 0 or removeTarget:
                self.visibleItems.pop(self.visibleItems.index(self.target))
                self.target = None

        else:
            self.wander()
        super(Carnivore, self).update()

    ################################
    def detect(self, cells):
        self.cs.updateVisibleItems(self)

        closestDist = 10000
        closest = None

        for stuff in self.visibleItems:
            dist = stuff.location.dist(self.location)
            if dist < closestDist and not type(stuff) is Plant and not type(stuff) is Carnivore:
                closestDist = dist
                closest = stuff

        if closest:
            self.target = closest



    #########################################
    def display(self):

        fill(0, 255, 0)
        fill(251, 0, 81)
        if self.detected:
            fill(255, 0, 0)
       
        pushMatrix()
        translate(self.location.x, self.location.y, self.location.z)
        noStroke()
        sphere(self.size)
        popMatrix()

        
        #fill(255, 0, 0, 10)
        #pushMatrix()
        #translate(self.location.x, self.location.y, self.location.z)
        #sphere(self.sightRange)
        # ellipse(self.location.x, self.location.y, self.sightRange, self.sightRange)
        #popMatrix()



