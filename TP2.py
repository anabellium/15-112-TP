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

        # if self.dx < 0: FLIP IMAGE WHEN MOVING LEFT
        #     sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)

        drawImage(sprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)
    
    def walking(self, app):
        self.xpos += self.dx


class Boy:
    pass

class Rival:
    pass

class Teacher: 
    pass


'''all graphics-functions here'''
def onAppStart(app):
    app.width = 500
    app.height = 500
    #make mc sprite
    mcstrip = openImage("C:/Users/Anabelle/Desktop/code/15-112/TP/TP2/spritestrip.png")
    app.mcsprites = []
    for i in range(6):
        mcFrame = CMUImage(mcstrip.crop((30+260*i, 30, 230+260*i, 250)))
        app.mcsprites.append(mcFrame)

    app.mc = MC(app.width/2, app.height/2, app.mcsprites)

    #miscellaneous variables
    app.spriteCounter = 0
    app.stepsPerSecond = 10

def redrawAll(app):
    app.mc.draw(app, app.mcsprites, app.spriteCounter)

def onStep(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.mcsprites)

def onMousePress(app, mouseX, mouseY):
    pass

def onMouseRelease(app, mouseX, mouseY):
    pass

def onKeyHold(app, keys):
    if 'd' in keys:
        app.mc.dx = 5
        app.mc.walking(app)
    elif 'a' in keys:
        app.mc.dx = -5
        app.mc.walking(app)

'''all helper functions here'''
def dist(x1, y1, x2, y2):
    return math.floor(math.sqrt((x2-x1)**2 + (y2-y1)**2))

def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def main():
    runApp()
runApp()