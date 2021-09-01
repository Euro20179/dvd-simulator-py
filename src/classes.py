import random
import pygame
from statistics import mean

class DVDS:
    def __init__(self, winWidth, winHeight, DVD_Logos, SH, SW, SX=False, SY=False, dispInfo=False, *args, **kwargs):
        DVDS.winWidth = winWidth
        DVDS.winHeight = winHeight
        DVDS.DVD_Logos = DVD_Logos
        if not SX:
            SX = random.randint(0, round(winWidth - SW))
            SY = random.randint(0, round(winHeight - SH))
        self.SX, self.SY = SX, SY
        self.SH, self.SW = SH, SW
        self.wallHits = 0
        self.SXGain = random.choice([(winWidth + winHeight) / 2 / 1300, -((winWidth + winHeight) / 2 / 1300)])
        self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(DVD_Logos)
        self.dispHits = True if kwargs.get("dispHits") else False
        self.dispXY = True if kwargs.get("dispXY") else False
        self.dispYSpeed = True if kwargs.get("dispYSpeed") else False
        self.dispXSpeed  = True if kwargs.get("dispXSpeed") else False
        self.Move = True

    @property
    def rect(self):
        return pygame.Rect(self.SX, self.SY, self.SW, self.SH)

    @property
    def dispInfo(self):
        return self.dispHits or self.dispXY or self.dispYSpeed or self.dispXSpeed

    @dispInfo.setter
    def dispInfo(self, val):
        self.__dispInfo = val

    def setDispInfo(self, b=None):
        self.dispInfo = b if b else self.dispInfo^True

    def setDispHits(self, b=None):
        self.dispHits = b if b else self.dispHits^True

    def setDispXY(self, b=None):
        self.dispXY = b if b else self.dispXY^True

    def setDispXSpeed(self, b=None):
        self.dispXSpeed = b if b else self.dispXSpeed^True

    def setDispYSpeed(self, b=None):
        self.dispYSpeed = b if b else self.dispYSpeed^True

    def setLogo(self, logo=None):
        self.currentLogo = logo if logo else random.choice(DVDS.DVD_Logos)

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

    def setSXGain(self, gain=None):
        if gain:
            self.SXGain = gain
        else:
            self.SXGain *= (-1 + random.uniform(-.1, .1))

    def setSYGain(self, gain=None):
        if gain:
            self.SYGain = gain
        else:
            self.SYGain *= (-1 + random.uniform(-.1, .1))

    def setMove(self, b=None):
        self.Move = b if b else self.Move^True
    
    def move(self): 
        if not self.Move:
            return
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
class InverseColorDVD(DVDS):
    def __init__(self, winWidth, winHeight, DVD_Logos, SH, SW, SX=None, SY=None, dispInfo=False, *args, **kwargs):
        super().__init__(winWidth, winHeight, DVD_Logos, SH, SW, SX=SX, SY=SY, dispInfo=dispInfo, *args, **kwargs)

    def recolorInverseDVDS(self, *args):
        DVDSList, inverseRGBColor, DVD_Logos = args
        s = DVD_Logos[0].copy()
        s.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        s.fill(inverseRGBColor + (0,), None, pygame.BLEND_RGBA_MAX)
        DVD_Logos.pop(-1)
        DVD_Logos.insert(-1, s)
        self.setLogo(DVD_Logos[-1])
        
        return DVDSList, DVD_Logos

        
class AvgPosDVD(DVDS):
    def __init__(self, winWidth, winHeight, DVD_Logos, SH, SW, SX=None, SY=None, dispInfo=[True]*2):
        super().__init__(winWidth, winHeight, DVD_Logos, SH, SW, SX=SX, SY=SY, dispInfo=[None]*4)
        self.dispInfo = dispInfo
        self.dispXY, self.dispXYDist = dispInfo

    def setDispXYDist(self, b=None):
        self.dispXYDist = b if b else self.dispXYDist^True

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
        
    def setOn(self, b=None):
        self.on = b if b else self.on^True

    def switch(self, keys):
        if keys[self.key]: self.setOn()

    @classmethod
    def setClsOn(cls, b=None):
        cls.On = b if b else cls.On^True

class VisualOptions(Options):
    def __init__(self, on, key, name):
        super().__init__(on, key, name, None, None)