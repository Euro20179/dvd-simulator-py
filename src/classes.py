import random
import pygame
from statistics import mean

class DVDS:
    def __init__(self, winWidth, winHeight, DVD_Logos, SH, SW, *args, SX=False, SY=False, dispInfo=[False] * 4):
        DVDS.winWidth = winWidth
        DVDS.winHeight = winHeight
        DVDS.DVD_Logos = DVD_Logos
        if not SX:
            SX = random.randint(0, round(winWidth - SW))
            SY = random.randint(0, round(winHeight - SH))
        self.SX, self.SY = SX, SY
        self.SH, self.SW = SH, SW
        self.wallHits = 0
        self.SXGain = random.choice([(winWidth + winHeight) / 2 / 1000, -((winWidth + winHeight) / 2 / 1000)])
        self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(DVD_Logos)
        self.dispHits, self.dispXY, self.dispXSpeed, self.dispYSpeed = dispInfo
        self.dispInfo = dispInfo
        self.Move = True
        if "inverseColor" in args:
            self.inverseColor = True
        else:
            self.inverseColor = False

    def setDispInfo(self, b=None):
        if b:
            self.dispInfo = b
        else:
            self.dispInfo = False if self.dispInfo else True

    def setDispHits(self, b=None):
        if b:
            self.dispHits = b
        else:
            self.dispHits = False if self.dispHits else True
    def setDispXY(self, b=None):
        if b:
            self.dispXY = b
        else:
            self.dispXY = False if self.dispXY else True
    def setDispXSpeed(self, b=None):
        if b:
            self.dispXSpeed = b
        else:
            self.dispXSpeed = False if self.dispXSpeed else True
    def setDispYSpeed(self, b=None):
        if b:
            self.dispYSpeed = b
        else:
            self.dispYSpeed = False if self.dispYSpeed else True

    def setLogo(self, logo=None):
        if not logo:
            self.currentLogo = random.choice(DVDS.DVD_Logos)
        else:
            self.currentLogo = logo

    def setSX(self, pos=None):
        if pos:
            self.SX = pos
        else:
            self.SX += self.SXGain

    def setSY(self, pos=None):
        if pos:
            self.SY = pos
        else:
            self.SY += self.SYGain

    def setSXGain(self):
        self.SXGain *= (-1 + random.uniform(-.1, .1))

    def setSYGain(self):
        self.SYGain *= (-1 + random.uniform(-.1, .1))

    def setMove(self, b=None):
        if b:
            self.Move = b
        else:
            self.Move = False if self.Move else True
    
    def move(self): 
        #moves the DVD around the screen
        self.setSX()
        self.setSY()

        #wall collision detection
        if self.SX <= 0 or self.SX + self.SW >= DVDS.winWidth:
            self.setSXGain()
            self.setLogo()
            self.wallHits += 1
            self.SX += self.SXGain / 2

        if self.SY <= 0 or self.SY + self.SH >= DVDS.winHeight:
            self.setSYGain()
            self.setLogo()
            self.wallHits += 1
            self.SY += self.SYGain / 2

    def findAVGPos(self, DVDSList):
        self.setSX(mean([x.SX for x in DVDSList]))
        self.setSY(mean([y.SY for y in DVDSList]))

class Options:
    On = True
    def __init__(self, on, key, name, xRend, yRend):
        self.on = on
        self.key = key
        self.name = name
        self.xRend = xRend
        self.yRend = yRend

    @classmethod
    def setClsOn(cls, b=None):
        if b:
            cls.On = b
        else:
            cls.On = False if cls.On else True
            
    def setOn(self, b=None):
        if b:
            self.on = b
        else:
            self.on = False if self.on else True

    def switch(self, keys):
        if keys[self.key]: self.setOn()

class VisualOptions(Options):
    def __init__(self, on, key, name):
        super().__init__(on, key, name, None, None)



