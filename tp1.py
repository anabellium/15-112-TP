from cmu_graphics import *
from PIL import Image
import os, pathlib
import random
import math

#create MC class
class MC:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.dx = 0
        self.width = 25
        self.height = 50 
        self.hp = 100
        self.attacking = False

    def draw(self, app, other):
        drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'pink',
                 align = 'center')
        drawLabel('MC: ' + str(self.hp), self.xpos, self.ypos)

        #lasers
        if self.attacking:
            drawLine(self.xpos, self.ypos, other.xpos, other.ypos, fill = 'red')

    def walking(self, app):
        self.xpos += self.dx
    
    def collision(self, app):
        self.hp -= 5
    
#create boys class
class Boy:
    def __init__(self, xpos, ypos):
        self.initX = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.follow = False
        self.dx = random.randint(1, 5)
        self.width = 25
        self.height = 50
        self.range = random.randint(20, 60)
        self.hp = 100

        self.beingAttacked = False
        self.Follow = False
    
    def draw(self, app):
        drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'blue', 
                 align = 'center')
        drawLabel('boy: ' + str(self.hp), self.xpos, self.ypos)
    
    def wander(self, app): #boys move on their own
        if not self.follow:
            self.xpos += self.dx
            if ((self.xpos > self.initX + self.range) or 
                (self.xpos < self.initX - self.range)):
                self.dx *= -1
    
    def healthDrain(self, app): #when attacked by mc, lose hp ---ask about mouseHold events
        if self.hp == 0:
            self.beingAttacked = False
            self.follow = True
        
        elif self.beingAttacked and self.hp > 0:
            self.hp -= 5

    def followMC(self, app, other):
        if self.follow:
            if other.dx > 0:
                self.xpos = other.xpos - 20
                self.ypos = other.ypos
            elif other.dx < 0:
                self.xpos = other.xpos + 20
                self.ypos = other.ypos
                
#create teacher class
class Teacher:
    def __init__(self, xpos, ypos):
        self.initX = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.width = 25
        self.height = 50
        self.range = random.randint(50, 100)
        self.dx = random.randint(3, 5)
    
    def draw(self, app):
        drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'green')
    
    def wander(self, app):
        self.xpos += self.dx
        if ((self.xpos > self.initX + self.range) or 
            (self.xpos < self.initX - self.range)):
            self.dx *= -1

#creating rival class
class Rival:
    def __init__(self, xpos, ypos):
        self.initX = xpos
        self.xpos = xpos
        self.ypos = ypos
        self.width = 25
        self.height = 50
        self.range = random.randint(50, 100)
        self.dx = random.randint(3, 5)

        self.attacking = False

    def draw(self, app):
        drawRect(self.xpos, self.ypos, self.width, self.height, fill = 'magenta')
        drawLabel('rival', self.xpos+10, self.ypos, align = 'center')
    
    def wander(self, app):
        self.xpos += self.dx
        if ((self.xpos > self.initX + self.range) or 
            (self.xpos < self.initX - self.range)):
            self.dx *= -1
    
    def attack(self, app, other):
        if self.attacking:
            print('entered')
            drawLine(self.xpos, self.ypos, other.xpos, other.ypos, fill = 'red')
            other.hp += 2

#graphics code starts here
def onAppStart(app):
    app.width = 1000
    app.height = 300
    app.mc = MC(app.width/2, app.height/2) #create mc object

    #create boys objects
    app.boys = list() 
    app.nboys = 5 #number of boys
    for i in range(app.nboys):
        app.boys.append(Boy(random.randint(0, app.width), random.randint(0, app.height)))
    
    #create teachers objects
    app.teachers = list()
    app.nteachers = 3
    for i in range(app.nteachers):
        app.teachers.append(Teacher(random.randint(0, app.width), random.randint(0, app.height)))

    #creates rivals objects
    app.rivals = list()
    app.nrivals = 4
    for i in range(app.nrivals):
        app.rivals.append(Rival(random.randint(0, app.width), random.randint(0, app.height)))
    
    #misc variables
    app.selectedBoy = 0
    app.gameOver = False
    app.detectRange = 20

    #scrolling variables
    app.scrollX = 0
    app.scrollMargin = 100

def makePlayerVisible(app):
    #scrolling, taken from 
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
    if (app.mc.xpos < app.scrollX + app.scrollMargin):
        app.scrollX = app.mc.xpos - app.scrollMargin
    if (app.mc.xpos > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.mc.xpos - app.width + app.scrollMargin

def redrawAll(app):
    # if app.mc.hp <= 0:
    #     drawRect(0, 0, app.width, app.height, fill = 'red')
    #     drawLabel('Game Over', app.width/2, app.height/2, align = 'center')
    
    # else:
    #background
    drawRect(0, 0, app.width, app.height, fill = 'gray')

    #draw mc, boys, rivals, and teachers
    app.mc.xpos -= app.scrollX
    app.mc.draw(app, app.boys[app.selectedBoy])

    for i in range(app.nboys):
        app.boys[i].xpos -= app.scrollX
        app.boys[i].draw(app)

    for i in range(app.nteachers):
        app.teachers[i].draw(app)
    
    for i in range(app.nrivals):
        app.rivals[i].draw(app)

def onKeyHold(app, keys):
    if 'a' in keys:
        app.mc.dx = -4
        app.mc.walking(app)

    elif 'd' in keys:
        app.mc.dx = 4
        app.mc.walking(app)

def onMousePress(app, mouseX, mouseY):
    for i in range(app.nboys): #if user clicks on boy, shoot lasers at boy
        if (dist(mouseX, mouseY, app.boys[i].xpos, app.boys[i].ypos) < 
            app.boys[i].width):

            app.selectedBoy = i
            app.mc.attacking = True
            app.boys[i].beingAttacked = True
            app.boys[i].healthDrain(app)
            app.boys[i].dx = 0

def onMouseRelease(app, mouseX, mouseY):
    app.mc.attacking = False

    #if boy still alive after attack, walks slower
    for i in range(app.nboys):
        if app.boys[i].beingAttacked == True and app.boys[i].hp > 0:
            app.boys[i].dx -= 2

def onStep(app):
    #boys and teachers walk around the halls
    for i in range(app.nboys):
        if not app.boys[i].follow:
            app.boys[i].wander(app)
        else:
            app.boys[i].followMC(app, app.mc)
    
    for i in range(app.nteachers):
        app.teachers[i].wander(app)

        #teacher-mc collision
        if (dist(app.teachers[i].xpos, app.teachers[i].ypos, app.mc.xpos, app.mc.ypos) <
            app.mc.width):
            app.mc.collision(app)
    
    for i in range(app.nrivals):
        app.rivals[i].wander(app)

        #mc-rival battle
        if ((dist(app.rivals[i].xpos, app.rivals[i].ypos, app.mc.xpos, app.mc.ypos) < app.detectRange)
            and (app.mc.attacking == True)):
            app.rivals[i].attacking = True
            app.rivals[i].attack(app, app.boys[app.selectedBoy])

#miscellaneous math functions
def dist(x1, y1, x2, y2):
    return math.floor(math.sqrt((x2-x1)**2 + (y2-y1)**2))

def main():
    runApp()

main()