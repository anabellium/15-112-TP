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
        self.width = 65
        self.height = 130

        self.hp = 100
        self.attacking = False
    
    def draw(self, app, sprites, flippedSprites, counter, other):
        sprite = sprites[counter]
        flippedSprite = flippedSprites[counter]

        if self.dx == 0:
            drawImage(sprites[1], self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)    

        elif self.dx < 0:
            drawImage(sprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)    

        else:
            drawImage(flippedSprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)    
        #lasers
        if self.attacking:
            drawLine(self.xpos+10, self.ypos-50, other.xpos, other.ypos-50, fill = 'red')
    
    def walking(self, app):
        self.xpos += self.dx

class Boy:
    def __init__(self, xpos, ypos):
        self.initx = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.width = 75
        self.height = 150
        self.dx = random.randint(1, 3)
        self.range = random.randint(30, 50)

        self.hp = 100
        self.follow = False
        self.beingAttacked = False
    
    def draw(self, app, sprites, flippedSprites, counter, other):
        #draws boy
        sprite = sprites[counter]
        flippedSprite = flippedSprites[counter]

        if not self.follow:
            if self.dx < 0:
                drawImage(flippedSprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                    width=self.width, height=self.height)    

            else:
                drawImage(sprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                  width=self.width, height=self.height)  

        else:
            #other is MC
            drawImage(sprites[1], other.xpos + 10, other.ypos, self.width, self.height)

    def wander(self, app, other):
        if not self.follow:
            self.xpos += self.dx
            if ((self.xpos > self.initx + self.range) or 
                (self.xpos < self.initx - self.range)):
                self.dx *= -1
    
    def healthDrain(self, app):
        if self.hp <= 0:
            self.beingAttacked = False
            self.follow = True
        
        elif self.beingAttacked and self.hp > 0:
            self.hp -= 5

class Rival:
    def __init__(self, xpos, ypos):
        self.initx = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.width = 75
        self.height = 150
        self.dx = random.randint(1, 3)
        self.range = random.randint(30, 50)

        self.hp = 100
        self.attacking = False
    
    def draw(self, app, sprites, flippedSprites, counter, other):
        #draws rival
        sprite = sprites[counter]
        flippedSprite = flippedSprites[counter]

        if self.dx < 0:
            drawImage(flippedSprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                width=self.width, height=self.height)    

        else:
            drawImage(sprite, self.xpos - self.width/2, self.ypos-self.height/2, 
                width=self.width, height=self.height)  

        if self.attacking:
            drawLine(self.xpos, self.ypos, other.xpos, other.ypos, fill = 'magenta')

    def wander(self, app):
        self.xpos += self.dx
        if ((self.xpos > self.initx + self.range) or 
            (self.xpos < self.initx - self.range)):
            self.dx *= -1
    
    def steal(self, app, other):
        if self.attacking: 
            other.hp += 3

    
'''all graphics-functions here'''
def onAppStart(app):
    app.width = 1000
    app.height = 500

    #load background image
    app.myBackground = openImage(r'background.jpg')  
    app.myBackground = CMUImage(app.myBackground.crop((0, 488, 728, 488)))

    #make mc sprite
    mcstrip = openImage(r'sprites\mc_sprites\mcspritesheet.png')  
    mcflippedStrip = openImage(r'sprites\mc_sprites\mcspritesheet.png')  
    mcflippedStrip = mcstrip.transpose(Image.FLIP_LEFT_RIGHT)
    
    app.mcflippedSprites = []
    app.mcsprites = []
    for i in range(6):
        mcFrame = CMUImage(mcstrip.crop((111*i, 0, 111+111*i, 278)))
        app.mcsprites.append(mcFrame)

        mcflippedFrame = CMUImage(mcflippedStrip.crop((111*i, 0, 111+111*i, 278)))
        app.mcflippedSprites.append(mcflippedFrame)

    app.mc = MC(app.width/2, app.height/2, app.mcsprites)

    #make boy1 sprite
    boy1strip = openImage(r'sprites\boy1sprites\boy1spritesheet.png')  
    boy1flippedStrip = openImage(r'sprites\boy1sprites\boy1spritesheet.png')  
    boy1flippedStrip = boy1strip.transpose(Image.FLIP_LEFT_RIGHT)
    
    app.boy1flippedSprites = []
    app.boy1sprites = []
    for i in range(23):
        boy1Frame = CMUImage(boy1strip.crop((236*i, 0, 236+236*i, 470)))
        app.boy1sprites.append(boy1Frame)

        boy1flippedFrame = CMUImage(boy1flippedStrip.crop((236*i, 0, 236+236*i, 470)))
        app.boy1flippedSprites.append(boy1flippedFrame)

#make rival4 sprite
    rival4strip = openImage(r'sprites\rival4sprites\rival4spritesheet.png')  
    rival4flippedStrip = openImage(r'sprites\rival4sprites\rival4spritesheet.png')  
    rival4flippedStrip =  rival4strip.transpose(Image.FLIP_LEFT_RIGHT)
    
    app. rival4flippedSprites = []
    app. rival4sprites = []
    for i in range(16):
        rival4Frame = CMUImage(rival4strip.crop((100*i, 0, 100+100*i, 278)))
        app.rival4sprites.append(rival4Frame)

        rival4flippedFrame = CMUImage(rival4flippedStrip.crop((100*i, 0, 100+100*i, 278)))
        app. rival4flippedSprites.append(rival4flippedFrame)

    #make boys
    app.allBoys = list() 
    app.nboys = 10 #number of boys
    for i in range(app.nboys):
        app.allBoys.append(Boy(random.randint(0, 5000), random.randint(0, app.height)))

    #make rivals
    app.allRivals = list()
    app.nrivals = 5 #number of rivals
    for i in range(app.nrivals):
        app.allRivals.append(Rival(random.randint(0, 5000), random.randint(0, app.height)))

    #miscellaneous variablesa
    app.spriteCounter = 0
    app.stepsPerSecond = 10
    app.mcX = app.mc.xpos
    app.selectedBoy = 0

    #sidescrolling variables
    app.scrollX = 0
    app.scrollMargin = 50

def redrawAll(app):
    #draw background
    # drawImage(app.myBackground, 0, 0, width = 1000, height = 500)

    #only displays the boys who are on the screen (sidescrolling)
    displayedBoys = list()
    for i in range(len(app.allBoys)):
        if app.allBoys[i] in displayedBoys:
            if ((displayedBoys[i].xpos > app.width) or (displayedBoys[i].xpos < 0)):
                displayedBoys.pop()
        else:
            displayedBoys.append(app.allBoys[i])

    #draw + scroll boys on screen
    for i in range(len(displayedBoys)):
        displayedBoys[i].xpos -= app.scrollX
        displayedBoys[i].draw(app, app.boy1sprites, app.boy1flippedSprites, app.spriteCounter, app.mc)
        displayedBoys[i].initx -= app.scrollX

    #only displays the rivals who are on the screen (sidescrolling)
    displayedRivals = list()
    for i in range(len(app.allRivals)):
        if app.allRivals[i] in displayedRivals:
            if ((displayedRivals[i].xpos > app.width) or (displayedRivals[i].xpos < 0)):
                displayedRivals.pop()
        else:
            displayedRivals.append(app.allRivals[i])

    #draw + scroll rivals on screen
    for i in range(len(displayedRivals)):
        displayedRivals[i].xpos -= app.scrollX
        displayedRivals[i].initx -= app.scrollX
        displayedRivals[i].draw(app, app.rival4sprites, app.rival4flippedSprites, app.spriteCounter, app.allBoys[app.selectedBoy])

    # draw mc
    app.mc.xpos -= app.scrollX # <-- scrolling the mc
    app.mc.draw(app, app.mcsprites, app.mcflippedSprites, app.spriteCounter,
                 app.allBoys[app.selectedBoy])

def onStep(app):
    app.spriteCounter = (app.spriteCounter + 1) % len(app.mcsprites) 

    for i in range(len(app.allBoys)):
        app.allBoys[i].wander(app, app.mc)

    for i in range(len(app.allRivals)):
        app.allRivals[i].wander(app)

def onMousePress(app, mouseX, mouseY):
    #if user clicks on boy, shoot lasers at boy
    for i in range(len(app.allBoys)): 
        if (dist(mouseX, mouseY, app.allBoys[i].xpos, app.allBoys[i].ypos) < 
            app.allBoys[i].width):
            app.selectedBoy = i
            app.mc.attacking = True
            app.allBoys[i].beingAttacked = True
            app.allBoys[i].healthDrain(app)
            app.allBoys[i].dx = 0
    
    #if rival notices mc attacking boy, shoot lasers as well
    for i in range(len(app.allRivals)):
        if ((dist(app.allRivals[i].xpos, app.allRivals[i].ypos, 
            app.allBoys[app.selectedBoy].xpos, app.allBoys[app.selectedBoy].ypos ) < 100) and
            (app.mc.attacking == True)):
            app.allRivals[i].attacking = True
            app.allRivals[i].steal(app, app.allBoys[app.selectedBoy])

def onMouseRelease(app, mouseX, mouseY):
    app.mc.attacking = False
    #if boy still alive after attack, walks slower
    for i in range(len(app.allBoys)):
        if app.allBoys[i].beingAttacked == True and app.allBoys[i].hp > 0:
            app.allBoys[i].dx -= 2

    #if rival attacking, stop
    for i in range(len(app.allRivals)):
        if app.allRivals[i].attacking:
            app.allRivals[i].attacking = False

def onKeyHold(app, keys):
    if 'd' in keys:
        app.mc.dx = 15
        app.mc.walking(app)
        app.scrollX = 5
 
    elif 'a' in keys:
        app.mc.dx = -15
        app.mc.walking(app)
        app.scrollX = -5
    
def onKeyRelease(app, key):
    if key == 'd':
        app.mc.dx = 0
        app.scrollX = 0
    elif key == 'a':
        app.mc.dx = 0
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
