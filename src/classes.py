import random
import pygame

class DVDS:
    def __init__(self, winWidth, winHeight, DVD_Logos, SH, SW, SX=False, SY=False, dispInfo=False):
        if not SX:
            SX = random.randint(0, round(winWidth - SW))
            SY = random.randint(0, round(winHeight - SH))
        self.SX, self.SY = SX, SY
        self.SH, self.SW = SH, SW
        self.wallHits = 0
        self.SXGain = random.choice([(winWidth + winHeight) / 2 / 1000, -((winWidth + winHeight) / 2 / 1000)]); self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(DVD_Logos)
        self.dispInfo = dispInfo
        self.Move = True
        
    def __call__(self, winWidth, winHeight, DVD_Logos): 
        #moves the DVD around the screen
        self.SX += self.SXGain
        self.SY += self.SYGain

        #wall collision detection
        if self.SX <= 0 or self.SX + self.SW >= winWidth:
            self.SXGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)
            self.wallHits += 1
            self.SX += self.SXGain / 2

        if self.SY <= 0 or self.SY + self.SH >= winHeight:
            self.SYGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)
            self.wallHits += 1
            self.SY += self.SYGain / 2

class Options:
    def __init__(self, on, key, name):
        self.on = on
        self.key = key
        self.name = name

    def switch(self, keys):
        if keys[self.key]: self.on = False if self.on else True

