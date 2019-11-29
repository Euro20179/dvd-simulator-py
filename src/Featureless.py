import pygame; pygame.init(); pygame.font.init(); pygame.mixer.init()
from os import listdir, environ
from tkinter.messagebox import showinfo
import random
from DVD_Screen import Menu
from sys import path
from Main import mainInit
import globalFuncs

def main(winWidth, winHeight, sh, sw):
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))
    Run = True
    path = "./DVD_Logos"
    sw, sh = int(sw), int(sh)
    logos = [str(f'{path}/{x}') for x in listdir(path)]
    DVD_Logos = [pygame.image.load(x) for x in logos]

    DVDSDict = {}

    swap = lambda: mainInit(winWidth, winHeight, sw, sh)

    class DVDS:
        def __init__(self, SX=False, SY=False, SH=sh, SW=sw):
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
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.display.quit(); pygame.quit(); Run = False; break
            if keys[pygame.K_PAUSE]:
                if keys[pygame.K_LSHIFT]: swap()
                else:
                    pygame.quit()
                    Menu().mainMenu()
            if keys[pygame.K_F12]: swap()
            if keys[pygame.K_F11]: globalFuncs.toggleFull(win)
                
            win.fill((0, 0, 0))
            for DVD in DVDSDict:
                DVDSDict[DVD]()
            for DVD in DVDSDict:
                win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
            pygame.display.update()