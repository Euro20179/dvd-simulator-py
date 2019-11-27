import pygame; pygame.init(); pygame.font.init(); pygame.mixer.init()
import sys
from os import listdir, environ
import tkinter as tk
from tkinter.messagebox import showinfo
import random
from statistics import mean
import time
sys.path.append(".\src")
import Menus

#MAIN MENU
DIMENSIONS = Menus.Menu()
DIMENSIONS.mainMenu()
winWidth = DIMENSIONS.winWidth
winHeight = DIMENSIONS.winHeight
SH = int(DIMENSIONS.picHeight)
SW = int(DIMENSIONS.picWidth)

#/Main Menu

#Center screen
environ['SDL_VIDEO_CENTERED'] = "1"

#FONTS
CTRLSFontSize = 20
addFont = pygame.font.SysFont("Alien Encounters", 20)
countFont = pygame.font.SysFont("Alien Encounters", 17)
controlsFont = pygame.font.SysFont("arial", CTRLSFontSize)
DVDInfoFont = pygame.font.SysFont("arial", 20)
leaderBoardFont = pygame.font.SysFont("Alien Encounters", 15)
avgHitsFont = pygame.font.SysFont("arial", 15)

#DVDLogos setup
path = "./DVD_Logos"

logos = [str(f'{path}/{x}') for x in listdir(path)]
DVD_Logos = [pygame.image.load(x) for x in logos]
DVDSDict = {}

#RANDOM VARS
Run = True

ADD = 1

leaders = 0

WFILLColor = [0, 0, 0]

#options
ShowLeader = False
ShowAdd = False
ShowTotal = False
ShowAVG = False
ShowRGB = False
ShowSum = False

if winWidth == 1920 and winHeight == 1080:
    FULLSCRN = True
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN, pygame.RESIZABLE)
else:
    FULLSCRN = False
    win = pygame.display.set_mode((winWidth, winHeight))

class DVDS:
    def __init__(self, SX=False, SY=False, SH=SH, SW=SW):
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

        if self.SY <= 0 or self.SY + self.SH >= winHeight:
            self.SYGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)
            self.wallHits += 1

        if self.SY <= 0 - self.SH or self.SY + self.SH >= winHeight + self.SH:
            self.SY = 1

        if self.SX <= 0 - self.SW or self.SX + self.SW >= winWidth + self.SW:
            self.SX = 1


DVDSDict[1] = DVDS()

def pygameMenus(screen):
    if FULLSCRN:
        with open(screen, "r") as CF:
            win.fill(tuple(WFILLColor))
            string = CF.read()
            string = string.split(chr(10))
            y = 0
            for line in string:
                win.blit(controlsFont.render(f'{line}', False, (0, 255, 255)), ((winWidth / 2) - (len(line) * (CTRLSFontSize / 5)), y))
                y += 17
            pygame.display.flip()
    else:
        if screen == "src/txt_files/controls.txt":
            controlsMenu()
        elif screen == "src/txt_files/info.txt":
            infoMenu()

def mainKeyChks():
    global ShowLeader, ShowTotal, ShowAdd, ShowAVG, ShowRGB, ShowSum, ADD, win, keys
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
        pygameMenus("src/txt_files/controls.txt")
    elif keys[pygame.K_F1]:
        pygameMenus("src/txt_files/info.txt")

    if keys[pygame.K_o] and keys[pygame.K_LSHIFT]:
        ShowAdd = True
        ShowAVG = True
        ShowLeader = True
        ShowRGB = True
        ShowSum = True
        ShowTotal = True
    if keys[pygame.K_o] and keys[pygame.K_LCTRL]:
        ShowAdd = False
        ShowAVG = False
        ShowLeader = False
        ShowRGB = False
        ShowSum = False
        ShowTotal = False
    if keys[pygame.K_h]:
        ShowLeader = False if ShowLeader else True
    if keys[pygame.K_t]:
        ShowTotal = False if ShowTotal else True
    if keys[pygame.K_a]:
        ShowAdd = False if ShowAdd else True
    if keys[pygame.K_m]:
        ShowAVG = False if ShowAVG else True
    if keys[pygame.K_F2]:
        ShowRGB = False if ShowRGB else True
    if keys[pygame.K_s]:
        ShowSum = False if ShowSum else True


    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]:
        pygame.mixer.Sound(".\src\Sounds\WINXP_Startup.wav").play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]:
        pygame.mixer.Sound(".\src\Sounds\THX_Sound.wav").play()


        
    if keys[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()
        Run = False
    if keys[pygame.K_PAUSE]:
        pygame.image.save(win, f'SCREENSHOTS\{time.time()}.jpeg')


while Run:
    clock = pygame.time.Clock()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            ADD = round(ADD)

            if event.button == 1:
                for a in range(ADD):
                    DVDSDict[len(DVDSDict) + 1] = DVDS()
                    if keys[pygame.K_LSHIFT]:
                        DVDSDict[len(DVDSDict)].dispInfo = True

            elif event.button == 3:
                MPos = pygame.mouse.get_pos()
                for DVD in DVDSDict:
                    if MPos[0] > DVDSDict[DVD].SX and MPos[0] < DVDSDict[DVD].SX + DVDSDict[DVD].SW and MPos[1] > DVDSDict[DVD].SY and MPos[1] < DVDSDict[DVD].SY + DVDSDict[DVD].SH:
                        DVDSDict[DVD].dispInfo = False if DVDSDict[DVD].dispInfo else True
                        break
                else:
                    for a in range(ADD):
                        pos = pygame.mouse.get_pos()
                        DVDSDict[len(DVDSDict) + 1] = DVDS(SX=pos[0], SY=pos[1])
                        if keys[pygame.K_LSHIFT]:
                            DVDSDict[len(DVDSDict)].dispInfo = True

            elif event.button == 2:
                if not keys[pygame.K_LSHIFT]:
                    for a in range(ADD):
                        try:
                            del DVDSDict[len(DVDSDict)]
                        except:
                            break
                else:
                    MPos = pygame.mouse.get_pos()
                    for DVD in DVDSDict:
                        if MPos[0] > DVDSDict[DVD].SX and MPos[0] < DVDSDict[DVD].SX + DVDSDict[DVD].SW and MPos[1] > DVDSDict[DVD].SY and MPos[1] < DVDSDict[DVD].SY + DVDSDict[DVD].SH:
                            temp = DVDSDict[len(DVDSDict)]
                            DVDSDict[len(DVDSDict)] = DVDSDict[DVD]
                            DVDSDict[DVD] = temp
                            del DVDSDict[len(DVDSDict)]
                            break
            
            elif event.button == 4 and keys[pygame.K_LSHIFT]:
                if keys[pygame.K_r] and WFILLColor[0] <= 245:
                    WFILLColor[0] += 10
                elif keys[pygame.K_g] and WFILLColor[1] <= 245:
                    WFILLColor[1] += 10
                elif keys[pygame.K_b] and WFILLColor[2] <= 245:
                    WFILLColor[2] += 10

                else:
                    ADD += 10

            elif event.button == 5 and keys[pygame.K_LSHIFT]:
                if WFILLColor[0] >= 10 and keys[pygame.K_r]:
                    WFILLColor[0] -= 10
                elif WFILLColor[1] >= 10 and keys[pygame.K_g]:
                    WFILLColor[1] -= 10
                elif WFILLColor[2] >= 10 and keys[pygame.K_b]:
                    WFILLColor[2] -= 10

                elif ADD >= 10:
                    ADD -= 10

            elif event.button == 4:
                if keys[pygame.K_r] and WFILLColor[0] <= 254:
                    WFILLColor[0] += 1
                elif keys[pygame.K_g] and WFILLColor[1] <= 254:
                    WFILLColor[1] += 1
                elif keys[pygame.K_b] and WFILLColor[2] <= 254:
                    WFILLColor[2] += 1

                else:
                    ADD += 1

            elif event.button == 5:
                if WFILLColor[0] >= 1 and keys[pygame.K_r]:
                    WFILLColor[0] -= 1
                elif WFILLColor[1] >= 1 and keys[pygame.K_g]:
                    WFILLColor[1] -= 1
                elif WFILLColor[2] >= 1 and keys[pygame.K_b]:
                    WFILLColor[2] -= 1

                elif ADD >= 1:
                    ADD -= 1

    if Run:
        hits = [x.wallHits for x in DVDSDict.values()]
        if hits:
            leaders = max(hits)
        temp = [x.wallHits for x in DVDSDict.values()]
        try:
            AVGHits = mean(temp)
            totalHits = sum(temp)
        except:
            pass

        mainKeyChks()

        for DVD in DVDSDict:
            DVDSDict[DVD]()
        if not keys[pygame.K_F1]:
            win.fill((WFILLColor[0], WFILLColor[1], WFILLColor[2]))
            if ShowAVG:
                avgWallHits = avgHitsFont.render(f'AVG HITS: {AVGHits}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(avgWallHits, (0, winHeight / 2))
            if ShowLeader:
                leaderBoardDisp = leaderBoardFont.render(f'MOST HITS: {leaders}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(leaderBoardDisp, (0, 90))
            if ShowAdd:
                add = addFont.render(f'ADD: {ADD}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(add, (0, 0))
            if ShowTotal:
                countTotal = countFont.render(f'DVDS: {len(DVDSDict)}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(countTotal, (0, 40))
            if ShowRGB:
                RGBDisp = avgHitsFont.render(f'RGB: {WFILLColor}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(RGBDisp, (0, 110))
            if ShowSum:
                sumDisp = countFont.render(f'TOTAL HITS: {totalHits}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                win.blit(sumDisp, (0, 70))
            for DVD in DVDSDict:
                win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
                if DVDSDict[DVD].dispInfo:
                    info = DVDInfoFont.render(f'wall hits: {DVDSDict[DVD].wallHits}', False, (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2]))
                    win.blit(info, (DVDSDict[DVD].SX + DVDSDict[DVD].SW, DVDSDict[DVD].SY))
            pygame.display.flip()
       