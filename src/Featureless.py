import pygame; pygame.init(); pygame.font.init(); pygame.mixer.init()
from os import listdir, environ
from tkinter.messagebox import showinfo
import random
from MovieBouncer2 import Menu

def main():
    winWidth = 1920
    winHeight = 1080
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN, pygame.RESIZABLE)
    Run = True
    path = "./DVD_Logos"

    logos = [str(f'{path}/{x}') for x in listdir(path)]
    DVD_Logos = [pygame.image.load(x) for x in logos]

    DVDSDict = {}

    class DVDS:
        def __init__(self, SX=False, SY=False, SH=97, SW=43):
            if not SX:
                SX = random.randint(0, round(winWidth - (.1 * winWidth)))
                SY = random.randint(0, round(winHeight - (.1 * winHeight)))
            self.SX = SX
            self.SY = SY
            self.SH = SH
            self.SW = SH
            self.wallHits = 0
            self.SXGain = random.choice([(winWidth + winHeight) / 2 / 700, -((winWidth + winHeight) / 2 / 700)]); self.SYGain = random.choice([self.SXGain, -self.SXGain])
            self.currentLogo = random.choice(DVD_Logos)
            self.dispInfo = False

        def __call__(self):
            self.SX += self.SXGain
            self.SY += self.SYGain

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


    DVDSDict[1] = DVDS()

    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                Run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    DVDSDict[len(DVDSDict) + 1] = DVDS()
                elif event.button == 2:
                    del DVDSDict[len(DVDSDict)]
                elif event.button == 3:
                    MPos = pygame.mouse.get_pos()
                    DVDSDict[len(DVDSDict) + 1] = DVDS(SX=MPos[0], SY=MPos[1])
        if Run:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.display.quit()
                pygame.quit()
                Run = False
                break
            if keys[pygame.K_PAUSE]: 
                pygame.quit(); Run = False
                Menu().mainMenu()
            win.fill((0, 0, 0))
            for DVD in DVDSDict:
                DVDSDict[DVD]()
            for DVD in DVDSDict:
                win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
            pygame.display.update()