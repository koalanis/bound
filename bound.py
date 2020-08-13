import pygame
import sys
import random
import math
from pygame.locals import *
from rich.console import Console


# ---------------------------------------------
# Line
# ---------------------------------------------
class Line:

  def __init__(self,w):
    self.line = list()
    self.bounds = list()
    self.width = w
    self.bounds.append((0,0))

  def addVertex(self,x,y):
    coor = (x,y)
    #print str(coor);
    self.bounds.insert(len(self.bounds)-1,coor)

  def isHit(self,xCoor,yCoor):
    hit = False
    x = 1

    while x<len(self.bounds) and not hit:
      hit = self.inLineZone(self.bounds[x][0],self.bounds[x][1],self.bounds[x-1][0],self.bounds[x-1][1],xCoor,yCoor)
      x=x+1
    return hit

  def changeCurrLoc(self,x,y):
    self.bounds[len(self.bounds)-1] = (x,y)

  def inLineZone(self, x1, y1, x2, y2, xLoc, yLoc):
    if x1==x2:
      if y1-y2>0:
        if xLoc==x1 and yLoc < y1 and yLoc > y2:
          return True
        else:
          return False
      elif y1-y2<0:
        if xLoc==x1 and yLoc < y2 and yLoc > y1:
          return True
        else:
          return False
    elif y1==y2:
      if x1-x2>0:
        if yLoc==y1 and xLoc < x1 and yLoc > x2:
         return True
        else:
         return False
      elif x1-x2<0:
        if yLoc==y1 and xLoc < x2 and xLoc >x1:
          return True
        else:
          return False

  def addDraw(self,x,y,color):
    data = (x,y,color)
    self.line.append(data)
  def drawLines(self, dispWindow):
    for n in self.line:
      pygame.draw.rect(dispWindow,n[2],(int(n[0]-self.width//2), int(n[1]-self.width//2), int(self.width), int(self.width)))
  def printBound(self):
    print(self.bounds)


# ---------------------------------------------
# Racer
# ---------------------------------------------
class Racer:

  player = 0
  xPos=0
  yPos=0
  color=(0,0,0)
  v = 2
  w = 6 # Width
  p = []
  angle = 180;
  t = False
  tc = (0,0,0)

  def __init__(self, x, y, color, player):
    self.xPos = x
    self.yPos = y
    self.color = color
    self.angle = 90
    self.p = player
    self.v=2
    self.w=6

  def move(self):
    self.xPos = self.xPos + math.cos(math.radians(self.angle))*self.v
    self.yPos = self.yPos + math.sin(math.radians(self.angle))*self.v

  def draw(self, dispWindow):
    pygame.draw.rect(dispWindow,self.color,(int(self.xPos-self.w//2), int(self.yPos-self.w//2), int(self.w), int(self.w)))


console = Console()


# ---------------------------------------------
# Game
# ---------------------------------------------
class Game: 
  
  def __init__(self):
    self.gameOn = False
    self.turnOff = False
    self.p1_controls = [K_d,K_a,K_s,K_w]
    self.p2_controls = [K_RIGHT,K_LEFT,K_DOWN,K_UP]    
    self.FPS = 30
    self.FPSCLOCK = pygame.time.Clock()
    self.HEIGHT = 600
    self.WIDTH  = 800
    self.dispWindow = pygame.display.set_mode((self.WIDTH,self.HEIGHT),0,32)
    self.p1Points = 0
    self.p2Points = 0
    self.redCount = 0
    self.bluCount = 0
  
  def init(self):
    self.blue = Racer(50,50,(0,0,150),self.p1_controls)
    self.red  = Racer(350,50,(150,0,0),self.p2_controls)
    self.bluBound = Line(2)
    self.redBound = Line(2)
    self.bluBound.addVertex(self.blue.xPos,self.blue.yPos)
    self.redBound.addVertex(self.red.xPos,self.red.yPos)
    self.gameOn = True

  def start(self):
   
    pygame.init()
    self.init()
    self.loop()
    pygame.quit()
  
  def loop(self):

    while not self.gameOver():
      self.update()
      self.draw()
      self.FPSCLOCK.tick(self.FPS)

  def controls(self, Racer,Line, event):
    if event.type==KEYDOWN and event.key == Racer.p[0]:
      if(math.sin(math.radians(Racer.angle))== 1.0):
        Racer.angle= Racer.angle-90
        Line.addVertex(Racer.xPos,Racer.yPos)

      if(math.sin(math.radians(Racer.angle))==-1.0):
        Racer.angle = Racer.angle+90
        Line.addVertex(Racer.xPos,Racer.yPos)

    if event.type==KEYDOWN and event.key == Racer.p[1]:
      if(math.sin(math.radians(Racer.angle))== 1.0):
        Racer.angle= Racer.angle+90
        Line.addVertex(Racer.xPos,Racer.yPos)
      if(math.sin(math.radians(Racer.angle))==-1.0):
        Racer.angle = Racer.angle-90
        Line.addVertex(Racer.xPos,Racer.yPos)

    if event.type==KEYDOWN and event.key == Racer.p[2]:
      if(math.cos(math.radians(Racer.angle))== 1.0):
        Racer.angle= Racer.angle+90
        Line.addVertex(Racer.xPos,Racer.yPos)
      if(math.cos(math.radians(Racer.angle))==-1.0):
        Racer.angle = Racer.angle-90
        Line.addVertex(Racer.xPos,Racer.yPos)

    if event.type==KEYDOWN and event.key == Racer.p[3]:
      if(math.cos(math.radians(Racer.angle))== 1.0):
        Racer.angle= Racer.angle-90
        Line.addVertex(Racer.xPos,Racer.yPos)
      if(math.cos(math.radians(Racer.angle))==-1.0):
        Racer.angle = Racer.angle+90
        Line.addVertex(Racer.xPos,Racer.yPos)

  def update(self):
    #handle events
    if self.gameOn: 
      for event in pygame.event.get():
        if event.type==QUIT:
          self.turnOff = True
          return

        self.controls(self.red,self.redBound, event)
        self.controls(self.blue,self.bluBound, event)

      self.red.move()
      self.redCount = self.redCount+1
      self.blue.move()
      self.bluCount = self.bluCount+1
      if self.redCount%10==0:
        self.redBound.changeCurrLoc(self.red.xPos,self.red.yPos)
      if self.bluCount%10==0:
        self.bluBound.changeCurrLoc(self.blue.xPos,self.blue.yPos)


      if(self.blue.xPos > self.WIDTH or self.blue.xPos < 0):
        self.p2Points = self.p2Points+1
        self.gameOn = False
      if(self.blue.yPos > self.WIDTH or self.blue.yPos < 0):
        self.p2Points = self.p2Points+1
        self.gameOn = False
      if(self.red.xPos > self.WIDTH or self.red.xPos < 0):
        self.p1Points = self.p1Points+1
        self.gameOn = False
      if(self.red.yPos > self.WIDTH or self.red.yPos < 0):
        self.p1Points = self.p1Points+1
        self.gameOn = False

      #print "red loc "+ str((red.xPos,blue.yPos))
      if self.redBound.isHit(self.red.xPos,self.red.yPos) or self.bluBound.isHit(self.red.xPos,self.red.yPos):
        self.p1Points = self.p1Points+1
        out = "p1 Hit - ("+str(self.red.xPos)+","+str(self.red.yPos)+")" 
        console.print(out, style="bold red")
        self.gameOn = False

      if self.redBound.isHit(self.blue.xPos,self.blue.yPos) or self.bluBound.isHit(self.blue.xPos,self.blue.yPos):
        self.p2Points = self.p2Points+1
        out = "blue Hit - ("+str(self.blue.xPos)+","+str(self.blue.yPos)+")"
        console.print(out, style="bold blue")
        self.gameOn = False
    else:
      self.init()

  def gameOver(self):
    return self.p1Points == 5 or self.p2Points == 5 or self.turnOff
      
  def draw(self):
    pygame.draw.rect(self.dispWindow,(255,255,255),(0,40, self.WIDTH,2))
    myfont = pygame.font.SysFont("monospace", 15)
    blueText = myfont.render("Player 1: "+ str(self.p1Points), 1, self.blue.color)
    redText = myfont.render("Player 2: "+str(self.p2Points),1,self.red.color)
    self.dispWindow.fill((0,0,0))
    self.dispWindow.blit(blueText,(0,20))
    self.dispWindow.blit(redText,(200,20))
    self.redBound.addDraw(self.red.xPos,self.red.yPos,self.red.color)
    self.bluBound.addDraw(self.blue.xPos,self.blue.yPos,self.blue.color)
    self.redBound.drawLines(self.dispWindow)
    self.bluBound.drawLines(self.dispWindow)
    self.red.draw(self.dispWindow)
    self.blue.draw(self.dispWindow)
    pygame.display.update() 


# ---------------------------------------------
# Main
# ---------------------------------------------
def main():

  game = Game()

  try:
    game.start()

  except Exception as e:
    print(e)

main()