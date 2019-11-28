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

FRAME = 0

#color settings

R, G, B = 0, 0, 0

baseColor = 255

inverseRGBColor = (255 - R, 255 - G, 255 - B)

SysFont = pygame.font.SysFont

#FONTS
CTRLSFontSize = 20
addFont = SysFont("Alien Encounters", 20)
countFont = SysFont("Alien Encounters", 17)
controlsFont = SysFont("arial", CTRLSFontSize)
DVDInfoFont = SysFont("arial", 20)
leaderBoardFont = SysFont("Alien Encounters", 15)
avgHitsFont = SysFont("arial", 15)

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

FULLSCRN, win = True if winWidth == 1920 and winHeight == 1080 else False, pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))

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
            self.SX += self.SXGain / 2

        if self.SY <= 0 or self.SY + self.SH >= winHeight:
            self.SYGain *= (-1 + random.uniform(-.1, .1))
            self.currentLogo = random.choice(DVD_Logos)
            self.wallHits += 1
            self.SY += self.SYGain / 2
        


DVDSDict[1] = DVDS()

def pygameMenus(screen):
    if FULLSCRN:
        with open(screen, "r") as CF:
            win.fill(tuple([R, G, B]))
            string = CF.read()
            string = string.split(chr(10))
            y = 0
            for line in string:
                win.blit(controlsFont.render(f'{line}', False, (0, 255, 255)), ((winWidth / 2) - (len(line) * (CTRLSFontSize / 5)), y))
                y += 17
            pygame.display.flip()
    else:
        if screen == "src/txt_files/controls.txt":
            Menus.infoMenu()
        elif screen == "src/txt_files/info.txt":
            Menus.controlsMenu()

def mainKeyChks(options, ADD, win):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEDOWN] and ADD >= 1:
        ADD -= 5
    if keys[pygame.K_PAGEUP]:
        ADD += 5
    if keys[pygame.K_END] and ADD >= 5:
        ADD -= 10
    if keys[pygame.K_HOME]:
        ADD += 10
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
    global R, G, B
    if R != baseColor and G != baseColor and B != baseColor:
        R = baseColor
        G = 0
        B = 0
    if R == baseColor and G >= 0 and B == 0 and G < baseColor:
        G += 1
    if R <= baseColor and G == baseColor and B == 0 and R > 0:
        R -= 1
    if R == 0 and G == baseColor and B >= 0 and B < baseColor:
        B += 1
    if R == 0 and G <= baseColor and B == baseColor and G > 0:
        G -= 1
    if R >= 0 and G == 0 and B == baseColor and R < baseColor:
        R += 1
    if R == baseColor and G == 0 and B <= baseColor and B > 0:
        B -= 1
    WFILLColor = [R, G, B]

while Run:
    clock = pygame.time.Clock()
    keys = pygame.key.get_pressed()
    FRAME += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break
        if event.type == pygame.KEYDOWN:
            options, ADD, win = mainKeyChks(options, ADD, win)
        if event.type == pygame.MOUSEBUTTONDOWN:
            ADD = round(ADD)
            MPos = pygame.mouse.get_pos()

            if event.button == 1:
                for a in range(ADD):
                    DVDSDict[len(DVDSDict) + 1] = DVDS()
                    if keys[pygame.K_LSHIFT]:
                        DVDSDict[len(DVDSDict)].dispInfo = True

            elif event.button == 2:
                if keys[pygame.K_LSHIFT]:
                    for DVD in DVDSDict:
                        if MPos[0] > DVDSDict[DVD].SX and MPos[0] < DVDSDict[DVD].SX + DVDSDict[DVD].SW and MPos[1] > DVDSDict[DVD].SY and MPos[1] < DVDSDict[DVD].SY + DVDSDict[DVD].SH:
                            temp = DVDSDict[len(DVDSDict)]
                            DVDSDict[len(DVDSDict)] = DVDSDict[DVD]
                            DVDSDict[DVD] = temp
                            del DVDSDict[len(DVDSDict)]
                            break

                else:
                    for a in range(ADD):
                        try:
                            del DVDSDict[len(DVDSDict)]
                        except:
                            break

            elif event.button == 3:
                for DVD in DVDSDict:
                    if MPos[0] > DVDSDict[DVD].SX and MPos[0] < DVDSDict[DVD].SX + DVDSDict[DVD].SW and MPos[1] > DVDSDict[DVD].SY and MPos[1] < DVDSDict[DVD].SY + DVDSDict[DVD].SH:
                        DVDSDict[DVD].dispInfo = False if DVDSDict[DVD].dispInfo else True
                        break
                else:
                    if keys[pygame.K_LCTRL]:
                        for DVD in DVDSDict: DVDSDict[DVD].dispInfo = False if DVDSDict[DVD].dispInfo else True

                    else:
                        for a in range(ADD):
                            DVDSDict[len(DVDSDict) + 1] = DVDS(SX=MPos[0], SY=MPos[1])
                            DVDSDict[len(DVDSDict)].dispInfo = True if keys[pygame.K_LSHIFT] else False
            
            elif event.button == 4:
                plus = 10 if keys[pygame.K_LSHIFT] else 1

                if keys[pygame.K_LCTRL] and baseColor <= 255 - plus:
                    baseColor += plus

                elif keys[pygame.K_r] and R <= 255 - plus:
                    R += plus
                elif keys[pygame.K_g] and G <= 255 - plus:
                    G += plus
                elif keys[pygame.K_b] and B <= 255 - plus:
                    B += plus

                else:
                    ADD += plus

            elif event.button == 5:
                plus = 10 if keys[pygame.K_LSHIFT] else 1
                if keys[pygame.K_LCTRL] and baseColor >= 10:
                    baseColor -= plus

                elif R >= 10 and keys[pygame.K_r]:
                    R -= plus
                elif G >= 10 and keys[pygame.K_g]:
                    G -= plus
                elif B >= 10 and keys[pygame.K_b]:
                    B -= plus

                elif ADD >= plus:
                    ADD -= plus

            

    else:
        pygame.key.set_repeat(5000, 5000)
        inverseRGBColor = (255 - R, 255 - G, 255 - B)
        if options["CycleColors"]:
            cycleColors()
        hits = [x.wallHits for x in DVDSDict.values()]
        if hits:
            leaders = max(hits)
            totalHits = sum(hits)
            AVGHits = mean(hits) if len(hits) >= 2 else totalHits

        for DVD in DVDSDict:
            DVDSDict[DVD]()
        if not keys[pygame.K_F1]:
            win.fill((R, G, B))
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
                RGBDisp = avgHitsFont.render(f'RGB: {R, G, B}', False, inverseRGBColor)
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
       