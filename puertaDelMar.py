import random
from CellSystem import CellSystem
from cell import Carnivore, Plant
from peasy import PeasyCam

cs = ''
stuffList = []
obstacles = []

totalCells = 15
totalPlants = 20
totalCarns = 0 

seasonLength = 1000
lastTime = 0
seasonChange = False
season = 0

import socket

UDP_IP = "192.168.1.102"
UDP_PORT = 30000
MESSAGE = "Hello, World!"

#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

camx = 0.005
cam = None

def setup():
    size(displayWidth, displayHeight, P3D)
    
    global cs, stuffList
    cs = CellSystem()

    import sys

    random.seed(1)
    for i in xrange(totalCells):
        cs.addRandomCell()

    
    for cell in cs.cells:
        stuffList.append(cell)

    cs.stuffList = stuffList
    global cam

    cam = PeasyCam(this, height/2, height/2, 500, 1800)
    
    #jhint(ENABLE_DEPTH_TEST) 
    # hint(ENABLE_DEPTH_SORT) 


    for i in xrange(totalPlants):
        stuffList.append(Plant(random.randint(25, height - 25), random.randint(25, height-25), random.randint(25, height-25)))


    for carn in xrange(totalCarns):
        carn = Carnivore(random.randint(25, height - 25), random.randint(25, height-25), random.randint(25, width - 25))
        carn.cs = cs
        carn.obstacles = obstacles
        stuffList.append(carn)

    hint(DISABLE_DEPTH_TEST)
    

def sketchFullScreen():
    return True

def draw():

    global camx, cam
    # Camera rotation
    #cam.rotateY(camx)
    
    background(25, 28, 31)
    carn = stuffList[0]
    # message = ','.join([str(carn.location.x), str(carn.location.y), str(carn.location.z), str(carn.velocity.x), str(carn.velocity.y), str(carn.velocity.z)])
    # sock.sendto(message, (UDP_IP, UDP_PORT))
    
    #rotateZ( map(mouseY,0,height,0,TWO_PI))
    #rotateY( map(mouseX,0,width, 0,TWO_PI))
    

    pushMatrix()
    translate(displayHeight/2, displayHeight/2, displayHeight/2)
    
    #fill(255, 0, 0)
    noFill()
    #stroke(255, 255, 209, 30)
    noStroke()
    translate(-displayHeight/2, displayHeight/2, - displayHeight/2)
    beginShape()
    fill(255, 0, 0)
    vertex(0, -displayHeight, 0)
    vertex(displayHeight, -displayHeight, 0)
    fill(0, 0, 255)
    vertex(displayHeight, 0, 0)
    vertex(0, 0, 0)
    endShape(CLOSE)
    beginShape()
    fill(255, 0, 0)
    vertex(0, -displayHeight, 0)
    vertex(0, -displayHeight, displayHeight)
    fill(0, 0, 255)
    vertex(0, 0, displayHeight)
    vertex(0, 0, 0)
    endShape(CLOSE)
    beginShape()
    fill(255, 0, 0)
    vertex(0, -displayHeight, 0)
    vertex(displayHeight, -displayHeight, 0)
    vertex(displayHeight, -displayHeight, displayHeight)
    vertex(0, -displayHeight, displayHeight) 
    endShape(CLOSE)
    # 2 more sides
    beginShape()
    fill(255, 0, 0)
    vertex(displayHeight, -displayHeight, 0)
    vertex(displayHeight, -displayHeight, displayHeight)
    fill(0, 0, 255)
    vertex(displayHeight, 0, displayHeight) 
    vertex(displayHeight, 0, 0)
    endShape(CLOSE)
    beginShape()
    fill(255, 0, 0)
    vertex(0, -displayHeight, displayHeight)
    vertex(displayHeight, -displayHeight, displayHeight)
    fill(0, 0, 255)
    vertex(displayHeight, 0, displayHeight) 
    vertex(0, 0, displayHeight)
    endShape(CLOSE)
    #
    beginShape()
    fill(0, 0, 255)
    vertex(0, 0, 0)
    vertex(displayHeight, 0, 0)
    vertex(displayHeight, 0, displayHeight)
    vertex(0, 0, displayHeight)
    endShape(CLOSE)

    #box(displayHeight)
    popMatrix()

    
    
    lights()
    ambientLight(102, 102, 102);

    # rotateY( map(mouseX,0,width,0,TWO_PI))

    for stuff in stuffList:
        # stuff.update()
        stuff.run()

    # cs.run()

    # sphere(cs.cells[0].size)


    
    global lastTime, seasonLength, seasonChange, season
    if millis() > lastTime + seasonLength:
        lastTime = millis()
        seasonChange = True

    if seasonChange:
        if season == 0:
            season = 1
        else:
            season = 0

        # for stuff in stuffList:
        #    if stuff.type == 'food':
        #        stuff.seasonChanged()

        seasonChange = False


    # fill(0, 0, 0, 255);
    noStroke();
    # rect(0, 0, width, height)
    


