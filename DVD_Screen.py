import pygame; pygame.init(); pygame.font.init(); pygame.mixer.init()
import sys
from os import listdir, environ
import tkinter as tk
from tkinter.messagebox import showinfo
import random
import Menus

#MAIN MENU
DIMENSIONS = Menus.Menu()
DIMENSIONS.mainMenu()
winWidth = DIMENSIONS.winWidth
winHeight = DIMENSIONS.winHeight

print(winWidth)

#/Main Menu

#Center screen
environ['SDL_VIDEO_CENTERED'] = "1"

#FONTS
CTRLSFontSize = 20
addFont = pygame.font.SysFont("Alien Encounters", 20)
countFont = pygame.font.SysFont("Alien Encounters", 17)
controlsFont = pygame.font.SysFont("arial", CTRLSFontSize)

#DVDLogos setup
path = "./DVD_Logos"

logos = [str(f'{path}/{x}') for x in listdir(path)]
DVD_Logos = [pygame.image.load(x) for x in logos]
DVDSDict = {}

#RANDOM VARS
Run = True
ADD = 1

if winWidth == 1920 and winHeight == 1080:
    FULLSCRN = True
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN)
else:
    FULLSCRN = False
    win = pygame.display.set_mode((winWidth, winHeight))

class DVDS:
    def __init__(self, SX=False, SY=False):
        if not SX:
            SX = random.randint(0, round(winWidth - (.1 * winWidth)))
            SY = random.randint(0, round(winHeight - (.1 * winHeight)))
        self.SX = SX
        self.SY = SY
        self.SH = 43
        self.SW = 98
        self.SXGain = random.choice([(winWidth + winHeight) / 2 / 1000, -((winWidth + winHeight) / 2 / 1000)]); self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(DVD_Logos)

    def __call__(self):
        self.SX += self.SXGain
        self.SY += self.SYGain

        if self.SX <= 0 or self.SX + self.SW >= winWidth:
            self.SXGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)

        if self.SY <= 0 or self.SY + self.SH >= winHeight:
            self.SYGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)

        if self.SXGain == 0:
            self.SX = winWidth / 2
            self.SY = winHeight / 2
            self.SXGain = 1
        if self.SYGain == 0:
            self.SX = winWidth / 2
            self.SY = winWidth / 2
            self.SYGain = 1
        if self.SX + self.SW > winWidth + 10 or self.SX < -10 or self.SY + self.SH > winHeight + 10 or self.SY < -10:
            self.SX = 100
            self.SY = 100

DVDSDict[1] = DVDS()

ShowAdd = True
ShowTotal = True

def pygameMenus(screen):
    if FULLSCRN:
        with open(screen, "r") as CF:
            win.fill((0, 0, 0))
            string = CF.read()
            string = string.split(chr(10))
            y = 0
            for line in string:
                win.blit(controlsFont.render(f'{line}', False, (0, 255, 255)), ((winWidth / 2) - (len(line) * (CTRLSFontSize / 5)), y))
                y += 17
            pygame.display.flip()
    else:
        if screen == "controls.txt":
            controlsMenu()
        elif screen == "info.txt":
            infoMenu()

while Run:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break
        print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
            ADD = round(ADD)
            if event.button == 1:
                for a in range(ADD):
                    DVDSDict[len(DVDSDict) + 1] = DVDS()

            elif event.button == 3:
                for a in range(ADD):
                    pos = pygame.mouse.get_pos()
                    DVDSDict[len(DVDSDict) + 1] = DVDS(SX=pos[0], SY=pos[1])

            elif event.button == 2:
                for a in range(ADD):
                    try:
                        del DVDSDict[len(DVDSDict)]
                    except:
                        break
            
            elif event.button == 4 and keys[pygame.K_LSHIFT]:
                ADD += 10
            elif event.button == 5 and keys[pygame.K_LSHIFT] and ADD >= 10:
                ADD -= 10
            elif event.button == 4:
                ADD += 1
            elif event.button == 5 and ADD >= 1:
                ADD -= 1
    if Run:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ADD += .1
        if keys[pygame.K_DOWN] and ADD >= .1:
            ADD -= .1
        if keys[pygame.K_PAGEDOWN] and ADD >= 1:
            ADD -= 1
        if keys[pygame.K_PAGEUP]:
            ADD += 1
        if keys[pygame.K_END] and ADD >= 5:
            ADD -= 5
        if keys[pygame.K_HOME]:
            ADD += 5
        if keys[pygame.K_F5]:
            DVDSDict.clear()

        if keys[pygame.K_F1] and keys[pygame.K_c]:
            pygameMenus("controls.txt")
        elif keys[pygame.K_F1]:
            pygameMenus("info.txt")


        if keys[pygame.K_t]:
            ShowTotal = False if ShowTotal else True

        if keys[pygame.K_a]:
            ShowAdd = False if ShowAdd else True

        if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]:
            pygame.mixer.Sound("Assets\Sounds\WINXP_Startup.wav").play()
        if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]:
            pygame.mixer.Sound("Assets\Sounds\THX_Sound.wav").play()


        
        if keys[pygame.K_ESCAPE] or keys[pygame.K_PAUSE]:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break


        for DVD in DVDSDict:
            DVDSDict[DVD]()
        if not keys[pygame.K_F1]:
            win.fill((0, 0, 0))
            add = addFont.render(f'ADD: {ADD}', False, (0, 255, 255))
            countTotal = countFont.render(f'TOTAL: {len(DVDSDict)}', False, (0, 255, 255))
            if ShowAdd:
                win.blit(add, (0, 0))
            if ShowTotal:
                win.blit(countTotal, (0, 40))

            for DVD in DVDSDict:
                win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
            pygame.display.flip()
        

    else:
        break