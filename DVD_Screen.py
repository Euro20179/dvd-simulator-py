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

#DVDLogos setup
path = "./DVD_Logos"

logos = [str(f'{path}/{x}') for x in listdir(path)]
DVD_Logos = [pygame.image.load(x) for x in logos]
DVDSDict = {}

#RANDOM VARS
Run = True

ADD = 1

leaders = 0



#color settings

WFILLColor = [0, 0, 0]

baseColor = 255

inverseRGBColor = (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2])

#FONTS
CTRLSFontSize = 20
addFont = pygame.font.SysFont("Alien Encounters", 20)
countFont = pygame.font.SysFont("Alien Encounters", 17)
controlsFont = pygame.font.SysFont("arial", CTRLSFontSize)
DVDInfoFont = pygame.font.SysFont("arial", 20)
leaderBoardFont = pygame.font.SysFont("Alien Encounters", 15)
avgHitsFont = pygame.font.SysFont("arial", 15)

#options
options = {
    "ShowLeader": False,
    "ShowAdd": False,
    "ShowTotal": False,
    "ShowAVG": False,
    "ShowRGB": False,
    "ShowSum": False,
    "CycleColors": False
    }

#sounds
sounds = {
    "windows": ".\src\Sounds\WINXP_Startup.wav",
    "THX": ".\src\Sounds\THX_Sound.wav"
    }


if winWidth == 1920 and winHeight == 1080:
    FULLSCRN = True
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN)
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

def mainKeyChks(options, ADD, win):
    
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
    if keys[pygame.K_F3]:
        options["CycleColors"] = True if not options["CycleColors"] else False

    if keys[pygame.K_F1] and keys[pygame.K_c]:
        pygameMenus("src/txt_files/controls.txt")
    elif keys[pygame.K_F1]:
        pygameMenus("src/txt_files/info.txt")

    if keys[pygame.K_o] and keys[pygame.K_LSHIFT]:
        for option in options:
            if option == "CycleColors":
                continue
            else:
                options[option] = True
    if keys[pygame.K_o] and keys[pygame.K_LCTRL]:
         for option in options:
            if option == "CycleColors":
                continue
            else:
                options[option] = False
    if keys[pygame.K_h]:
        options["ShowLeader"] = False if options["ShowLeader"] else True
    if keys[pygame.K_t]:
        options["ShowTotal"] = False if options["ShowTotal"] else True
    if keys[pygame.K_a]:
        options["ShowAdd"] = False if options["ShowAdd"] else True
    if keys[pygame.K_m]:
        options["ShowAVG"] = False if options["ShowAVG"] else True
    if keys[pygame.K_F2]:
        options["ShowRGB"] = False if options["ShowRGB"] else True
    if keys[pygame.K_s]:
        options["ShowSum"] = False if options["ShowSum"] else True


    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]:
        pygame.mixer.Sound(sounds["windows"]).play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]:
        pygame.mixer.Sound(sounds["THX"]).play()


        
    if keys[pygame.K_ESCAPE]:
        pygame.display.quit()
        pygame.quit()
        Run = False
    if keys[pygame.K_PAUSE]:
        pygame.image.save(win, f'SCREENSHOTS\{time.time()}.jpeg')

    return options, ADD, win

def cycleColors():
    R = WFILLColor[0]
    G = WFILLColor[1]
    B = WFILLColor[2]
    if R != baseColor and G != baseColor and B != baseColor:
        WFILLColor[0] = baseColor
        WFILLColor[1] = 0
        WFILLColor[2] = 0
    if R == baseColor and G >= 0 and B == 0 and G < baseColor:
        WFILLColor[1] += 1
    if R <= baseColor and G == baseColor and B == 0 and R > 0:
        WFILLColor[0] -= 1
    if R == 0 and G == baseColor and B >= 0 and B < baseColor:
        WFILLColor[2] += 1
    if R == 0 and G <= baseColor and B == baseColor and G > 0:
        WFILLColor[1] -= 1
    if R >= 0 and G == 0 and B == baseColor and R < baseColor:
        WFILLColor[0] += 1
    if R == baseColor and G == 0 and B <= baseColor and B > 0:
        WFILLColor[2] -= 1

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
            
            elif event.button == 4:
                plus = 10 if keys[pygame.K_LSHIFT] else 1

                if keys[pygame.K_LCTRL] and baseColor <= 245:
                    baseColor += plus

                elif keys[pygame.K_r] and WFILLColor[0] <= 245:
                    WFILLColor[0] += plus
                elif keys[pygame.K_g] and WFILLColor[1] <= 245:
                    WFILLColor[1] += plus
                elif keys[pygame.K_b] and WFILLColor[2] <= 245:
                    WFILLColor[2] += plus

                else:
                    ADD += plus

            elif event.button == 5:
                plus = 10 if keys[pygame.K_LSHIFT] else 1
                if keys[pygame.K_LCTRL] and baseColor >= 10:
                    baseColor -= plus

                elif WFILLColor[0] >= 10 and keys[pygame.K_r]:
                    WFILLColor[0] -= plus
                elif WFILLColor[1] >= 10 and keys[pygame.K_g]:
                    WFILLColor[1] -= plus
                elif WFILLColor[2] >= 10 and keys[pygame.K_b]:
                    WFILLColor[2] -= plus

                elif ADD >= 10:
                    ADD -= plus

    if Run:
        inverseRGBColor = (255 - WFILLColor[0], 255 - WFILLColor[1], 255 - WFILLColor[2])
        if options["CycleColors"]:
            cycleColors()
        hits = [x.wallHits for x in DVDSDict.values()]
        if hits:
            leaders = max(hits)
        temp = [x.wallHits for x in DVDSDict.values()]
        try:
            AVGHits = mean(temp)
            totalHits = sum(temp)
        except:
            pass

        options, ADD, win = mainKeyChks(options, ADD, win)

        for DVD in DVDSDict:
            DVDSDict[DVD]()
        if not keys[pygame.K_F1]:
            win.fill((WFILLColor[0], WFILLColor[1], WFILLColor[2]))
            if options["ShowAVG"]:
                avgWallHits = avgHitsFont.render(f'AVG HITS: {AVGHits}', False, inverseRGBColor)
                win.blit(avgWallHits, (0, winHeight / 2))
            if options["ShowLeader"]:
                leaderBoardDisp = leaderBoardFont.render(f'MOST HITS: {leaders}', False, inverseRGBColor)
                win.blit(leaderBoardDisp, (0, 90))
            if options["ShowAdd"]:
                add = addFont.render(f'ADD: {ADD}', False, inverseRGBColor)
                win.blit(add, (0, 0))
            if options["ShowTotal"]:
                countTotal = countFont.render(f'DVDS: {len(DVDSDict)}', False, inverseRGBColor)
                win.blit(countTotal, (0, 40))
            if options["ShowRGB"]:
                RGBDisp = avgHitsFont.render(f'RGB: {WFILLColor}', False, inverseRGBColor)
                RGBBaseDisp = avgHitsFont.render(f'RGB Base: {baseColor}', False, inverseRGBColor)
                win.blit(RGBDisp, (0, 110))
                win.blit(RGBBaseDisp, (0, 130))
            if options["ShowSum"]:
                sumDisp = countFont.render(f'TOTAL HITS: {totalHits}', False, inverseRGBColor)
                win.blit(sumDisp, (0, 70))
            for DVD in DVDSDict:
                win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
                if DVDSDict[DVD].dispInfo:
                    info = DVDInfoFont.render(f'wall hits: {DVDSDict[DVD].wallHits}', False, inverseRGBColor)
                    win.blit(info, (DVDSDict[DVD].SX + DVDSDict[DVD].SW, DVDSDict[DVD].SY))
            pygame.display.flip()
       