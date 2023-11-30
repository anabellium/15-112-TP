from cmu_graphics import *
from PIL import Image
import os, pathlib
import random
import math

'''all classes created here'''
class MC:
    def __init__(self, xpos, ypos, image):
        self.xpos = xpos
        self.ypos = ypos
        self.dx = 0
        self.width = 50
        self.height = 75

        self.image = image

        self.hp = 100
        self.attacking = False
    
    def draw(self, app, sprites, counter):
        sprite = sprites[counter]

        # if self.dx < 0:
        #     sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)

        drawImage(sprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)

        # drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'pink', align = 'center')
    
    
    def walking(self, app):
        self.xpos += self.dx

class Boy:
    def __init__(self, xpos, ypos):
        self.initx = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.width = 25
        self.height = 50
        self.dx = random.randint(1, 4)
        self.range = random.randint(5, 10)

        self.hp = 100
        self.follow = False
        self.beingAttacked = False
    
    def draw(self, app, other):
        #draws boy
        if not self.follow:
            drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'blue', align = 'center')
        
        else:
            #other is MC
            drawRect(other.xpos + 10, other.ypos, self.width, self.height, fill = 'blue', align = 'center')
        
    def wander(self, app, other):
        if not self.follow:
            if ((self.initx + self.xpos > self.range) or
                (self.initx - self.xpos < self.range)):
                self.dx *= -1
            self.xpos += self.dx

class Teacher: 
    pass

'''all graphics-functions here'''
def onAppStart(app):
    app.width = 1000
    app.height = 500
    #make mc sprite
    mcstrip = openImage(r'spritestrip.png')
    app.mcsprites = []
    for i in range(6):
        mcFrame = CMUImage(mcstrip.crop((30+260*i, 30, 230+260*i, 250)))
        app.mcsprites.append(mcFrame)

    app.mc = MC(app.width/2, app.height/2, app.mcsprites)

    #make boys
    app.allBoys = list() 
    app.displayedBoys = list()
    app.nboys = 5 #number of boys
    for i in range(app.nboys):
        app.allBoys.append(Boy(random.randint(0, app.width), random.randint(0, app.height)))

    for i in range(app.nboys):
        app.displayedBoys.append(app.allBoys[i])    

    #miscellaneous variables
    app.spriteCounter = 0
    app.stepsPerSecond = 10
    app.mcX = app.mc.xpos

    #sidescrolling variables
    app.scrollX = 0
    app.scrollMargin = 50

def redrawAll(app):
    #only displays the boys who are on the screen (sidescrolling)
    for i in range(len(app.allBoys)):
        if app.allBoys[i] in app.displayedBoys:
            if ((app.displayedBoys[i].xpos > app.width) or (app.displayedBoys[i].xpos < 0)):
                app.displayedBoys.pop(i)
        app.displayedBoys.append(app.allBoys[i])

    #draw + scroll boys on screen
    for i in range(len(app.displayedBoys)):
        app.displayedBoys[i].xpos -= app.scrollX
        app.displayedBoys[i].draw(app, app.mc)

    # draw mc
    app.mc.xpos -= app.scrollX # <-- scrolling the mc
    app.mc.draw(app, app.mcsprites, app.spriteCounter)

def onStep(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.mcsprites)

def onMousePress(app, mouseX, mouseY):
    #mc shoot lasers at rivals
    #rivals detect if mc shooting lasers
        #rivals shoot lasers
    pass

def onMouseRelease(app, mouseX, mouseY):
    #mc stops shooting lasers
    #rivals stop shooting lasers
    pass

def onKeyHold(app, keys):
    if 'd' in keys:
        app.mc.dx = 5
        app.mc.walking(app)
        app.scrollX = 5
    elif 'a' in keys:
        app.mc.dx = -5
        app.mc.walking(app)
        app.scrollX = -5


def onKeyRelease(app, key):
    if key == 'd':
        app.scrollX = 0
    elif key == 'a':
        app.scrollX = 0

'''all helper functions here'''
def dist(x1, y1, x2, y2):
    return math.floor(math.sqrt((x2-x1)**2 + (y2-y1)**2))

def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def makePlayerVisible(app):
    if (app.mcX < app.scrollX + app.scrollMargin):
        app.scrollX = app.playerX - app.scrollMargin
    if (app.playerX > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.playerX - app.width + app.scrollMargin

def main():
    runApp()
runApp()
