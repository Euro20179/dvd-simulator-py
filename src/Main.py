import sys
import time
import random
import pygame
import tkinter as tk
from Dvds import DVDS
from statistics import mean
from MovieBouncer2 import Menu
from os import listdir, environ
from tkinter.messagebox import showinfo

#this looks really nice tbh

#MAIN MENU
def VARS(winWidth, winHeight, SH, SW):
    winWidth, winHeight = winWidth, winHeight
    SH, SW = SH, SW

    pygame.init(); pygame.font.init(); pygame.mixer.init()

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

    R, G, B = 0, 0, 0; baseColor = 255
    inverseRGBColor = (255 - R, 255 - G, 255 - B)

    SysFont = pygame.font.SysFont

    #FONTS
    FSize20 = 20
    fonts = {
        "addFont": SysFont("Alien Encounters", FSize20),
        "countFont": SysFont("Alien Encounters", FSize20),
        "DVDInfoFont": SysFont("arial", 15),
        "leaderBoardFont": SysFont("Alien Encounters", FSize20),
        }

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
    sounds = {"windows": ".\src\Sounds\WINXP_Startup.wav", "THX": ".\src\Sounds\THX_Sound.wav"}

    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))

    return winWidth, winHeight, DVD_Logos, DVDSDict, Run ,ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, win, SH, SW


def mainKeyChks(VAR):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_PAGEDOWN] and VAR["ADD"] >= 1: VAR["ADD"] -= 5 
    if keys[pygame.K_PAGEUP]: VAR["ADD"] += 5  
    if keys[pygame.K_END] and VAR["ADD"] >= 5: VAR["ADD"] -= 10     
    if keys[pygame.K_HOME]: VAR["ADD"] += 10   
    if keys[pygame.K_F5]: VAR["DVDSDict"].clear()     
    if keys[pygame.K_F6]: VAR["options"]["CycleColors"] = True if not VAR["options"]["CycleColors"] else False
        
    if keys[pygame.K_F3]:
        for option in VAR["options"]:
            if option != "CycleColors": VAR["options"][option] = True if not VAR["options"][option] else False

    if keys[pygame.K_h]: VAR["options"]["ShowLeader"] = False if VAR["options"]["ShowLeader"] else True      
    if keys[pygame.K_t]: VAR["options"]["ShowTotal"] = False if VAR["options"]["ShowTotal"] else True      
    if keys[pygame.K_a]: VAR["options"]["ShowAdd"] = False if VAR["options"]["ShowAdd"] else True       
    if keys[pygame.K_m]: VAR["options"]["ShowAVG"] = False if VAR["options"]["ShowAVG"] else True       
    if keys[pygame.K_F4]: VAR["options"]["ShowRGB"] = False if VAR["options"]["ShowRGB"] else True
    if keys[pygame.K_s]: VAR["options"]["ShowSum"] = False if VAR["options"]["ShowSum"] else True
        
    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]: pygame.mixer.Sound(VAR["sounds"]["windows"]).play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]: pygame.mixer.Sound(VAR["sounds"]["THX"]).play()   
  
    if keys[pygame.K_ESCAPE]: pygame.quit(); pygame.display.quit(); VAR["Run"] = False
    if keys[pygame.K_PAUSE]: 
        pygame.quit(); VAR["Run"] = False
        Menu().mainMenu()

    if keys[pygame.K_F2]: pygame.image.save(VAR["win"], f'SCREENSHOTS\{time.time()}.jpeg')

    return VAR

def mouseChks(VAR, event):
    VAR["ADD"] = round(VAR["ADD"])

    MPos, keys = pygame.mouse.get_pos(), pygame.key.get_pressed()

    if event.button == 1:
        for a in range(VAR["ADD"]):
            VAR["DVDSDict"][len(VAR["DVDSDict"]) + 1] = DVDS(VAR, VAR["SH"], VAR["SW"])
            if keys[pygame.K_LSHIFT]: VAR["DVDSDict"][len(VAR["DVDSDict"])].dispInfo = True

    elif event.button == 2:
        if keys[pygame.K_LSHIFT]:
            for DVD in VAR["DVDSDict"]:
                if MPos[0] > VAR["DVDSDict"][DVD].SX and MPos[0] < VAR["DVDSDict"][DVD].SX + VAR["DVDSDict"][DVD].SW and MPos[1] > VAR["DVDSDict"][DVD].SY and MPos[1] < VAR["DVDSDict"][DVD].SY + VAR["DVDSDict"][DVD].SH:
                    temp = VAR["DVDSDict"][len(VAR["DVDSDict"])]
                    VAR["DVDSDict"][len(VAR["DVDSDict"])] = VAR["DVDSDict"][DVD]
                    VAR["DVDSDict"][DVD] = temp
                    del VAR["DVDSDict"][len(VAR["DVDSDict"])]
                    break

        else:
            for a in range(VAR["ADD"]):
                if len(VAR["DVDSDict"]) >= 1: del VAR["DVDSDict"][len(VAR["DVDSDict"])]

    elif event.button == 3:
        for DVD in VAR["DVDSDict"]:
            if MPos[0] > VAR["DVDSDict"][DVD].SX and MPos[0] < VAR["DVDSDict"][DVD].SX + VAR["DVDSDict"][DVD].SW and MPos[1] > VAR["DVDSDict"][DVD].SY and MPos[1] < VAR["DVDSDict"][DVD].SY + VAR["DVDSDict"][DVD].SH:
                VAR["DVDSDict"][DVD].dispInfo = False if VAR["DVDSDict"][DVD].dispInfo else True
                break
        else:
            if keys[pygame.K_LSHIFT]:
                for DVD in VAR["DVDSDict"]: VAR["DVDSDict"][DVD].dispInfo = False if VAR["DVDSDict"][DVD].dispInfo else True

            else:
                for a in range(VAR["ADD"]):
                    VAR["DVDSDict"][len(VAR["DVDSDict"]) + 1] = DVDS(VAR, VAR["SH"], VAR["SW"], SX=MPos[0], SY=MPos[1])
                    VAR["DVDSDict"][len(VAR["DVDSDict"])].dispInfo = True if keys[pygame.K_LSHIFT] else False
            
    elif event.button == 4:
        plus = 10 if keys[pygame.K_LSHIFT] else 1

        if keys[pygame.K_LCTRL] and VAR["baseColor"] <= 255 - plus: VAR["baseColor"] += plus
            
        elif keys[pygame.K_r] and VAR["R"] <= 255 - plus: VAR["R"] += plus       
        elif keys[pygame.K_g] and VAR["G"] <= 255 - plus: VAR["G"] += plus
        elif keys[pygame.K_b] and VAR["B"] <= 255 - plus: VAR["B"] += plus
           
        else:
            VAR["ADD"] += plus

    elif event.button == 5:
        plus = 10 if keys[pygame.K_LSHIFT] else 1

        if keys[pygame.K_LCTRL] and VAR["baseColor"] >= plus: VAR["baseColor"] -= plus

        elif VAR["R"] >= plus and keys[pygame.K_r]: VAR["R"] -= plus 
        elif VAR["G"] >= plus and keys[pygame.K_g]: VAR["G"] -= plus          
        elif VAR["B"] >= plus and keys[pygame.K_b]: VAR["B"] -= plus

        elif VAR["ADD"] >= plus: VAR["ADD"] -= plus

    return VAR

def cycleColors(VAR):
    if VAR["R"] != VAR["baseColor"] and VAR["G"] != VAR["baseColor"] and VAR["B"] != VAR["baseColor"]:
        VAR["R"] = VAR["baseColor"]
        VAR["G"] = 0
        VAR["B"] = 0

    if VAR["R"] == VAR["baseColor"] and VAR["G"] >= 0 and VAR["B"] == 0 and VAR["G"] < VAR["baseColor"]: VAR["G"] += 1    
    if VAR["R"] <= VAR["baseColor"] and VAR["G"] == VAR["baseColor"] and VAR["B"] == 0 and VAR["R"] > 0: VAR["R"] -= 1      
    if VAR["R"] == 0 and VAR["G"] == VAR["baseColor"] and VAR["B"] >= 0 and VAR["B"] < VAR["baseColor"]: VAR["B"] += 1 
    if VAR["R"] == 0 and VAR["G"] <= VAR["baseColor"] and VAR["B"] == VAR["baseColor"] and VAR["G"] > 0: VAR["G"] -= 1 
    if VAR["R"] >= 0 and VAR["G"] == 0 and VAR["B"] == VAR["baseColor"] and VAR["R"] < VAR["baseColor"]: VAR["R"] += 1
    if VAR["R"] == VAR["baseColor"] and VAR["G"] == 0 and VAR["B"] <= VAR["baseColor"] and VAR["B"] > 0: VAR["B"] -= 1
        
    return VAR

def main(vars):
    winWidth, winHeight, DVD_Logos, DVDSDict, Run ,ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, win, SH, SW = vars
    vars = {"winWidth": winWidth,
    "winHeight": winHeight,
    "DVD_Logos": DVD_Logos,
    "DVDSDict": DVDSDict,
    "Run": Run,
    "ADD": ADD,
    "leaders": leaders,
    "R": R,
    "G": G,
    "B": B,
    "baseColor": baseColor,
    "inverseRGBColor": inverseRGBColor,
    "fonts": fonts,
    "options": options,
    "sounds": sounds,
    "win": win,
    "SH": SH,
    "SW": SW}
    vars["DVDSDict"][1] = DVDS(vars, vars["SH"], vars["SW"])

    while Run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.display.quit(); pygame.quit(); vars["Run"] = False; break
            if event.type == pygame.KEYDOWN: vars = mainKeyChks(vars)  
            if event.type == pygame.MOUSEBUTTONDOWN: vars = mouseChks(vars, event)    
            
        else:
            vars["inverseRGBColor"] = (255 - vars["R"], 255 - vars["G"], 255 - vars["B"])

            if vars["options"]["CycleColors"]: vars = cycleColors(vars)  

            hits = [x.wallHits for x in vars["DVDSDict"].values()]
            if hits:
                vars["leaders"] = max(hits)
                totalHits = sum(hits)
                AVGHits = mean(hits) if len(hits) >= 2 else totalHits

            #rendering
            for DVD in vars["DVDSDict"].values(): DVD(vars)

            fonts = vars["fonts"]

            vars["win"].fill((vars["R"], vars["G"], vars["B"]))

            if vars["options"]["ShowAdd"]:
                add = fonts["addFont"].render(f'ADD: {vars["ADD"]}', False, vars["inverseRGBColor"])
                vars["win"].blit(add, (0, 0))

            if vars["options"]["ShowTotal"]:
                countTotal = fonts["countFont"].render(f'DVDS: {len(vars["DVDSDict"])}', False, vars["inverseRGBColor"])
                vars["win"].blit(countTotal, (0, 20))

            if vars["options"]["ShowSum"]:
                sumDisp = fonts["countFont"].render(f'TOTAL HITS: {totalHits}', False, vars["inverseRGBColor"])
                vars["win"].blit(sumDisp, (0, 40))

            if vars["options"]["ShowLeader"]:
                leaderBoardDisp = fonts["leaderBoardFont"].render(f'MOST HITS: {vars["leaders"]}', False, vars["inverseRGBColor"])
                vars["win"].blit(leaderBoardDisp, (0, 60))

            if vars["options"]["ShowRGB"]:
                RGBDisp = fonts["DVDInfoFont"].render(f'RGB: {vars["R"], vars["G"], vars["B"]}', False, vars["inverseRGBColor"])
                RGBBaseDisp = fonts["DVDInfoFont"].render(f'RGB Base: {vars["baseColor"]}', False, vars["inverseRGBColor"])
                vars["win"].blit(RGBDisp, (0, 80))
                vars["win"].blit(RGBBaseDisp, (0, 100))

            if vars["options"]["ShowAVG"]:
                avgWallHits = fonts["DVDInfoFont"].render(f'AVG HITS: {AVGHits}', False, vars["inverseRGBColor"])
                vars["win"].blit(avgWallHits, (0, 130))

            for DVD in vars["DVDSDict"]:
                vars["win"].blit(vars["DVDSDict"][DVD].currentLogo, (vars["DVDSDict"][DVD].SX, vars["DVDSDict"][DVD].SY))
                if vars["DVDSDict"][DVD].dispInfo:
                    info = fonts["DVDInfoFont"].render(f'wall hits: {vars["DVDSDict"][DVD].wallHits}', False, vars["inverseRGBColor"])
                    vars["win"].blit(info, (vars["DVDSDict"][DVD].SX + vars["DVDSDict"][DVD].SW, vars["DVDSDict"][DVD].SY))
            pygame.display.flip()

def mainInit(winWidth, winHeight, sh, sw):
    global SH, SW; SH, SW = int(sh), int(sw)
    VAR = VARS(winWidth, winHeight, SH, SW)
    main(VAR)