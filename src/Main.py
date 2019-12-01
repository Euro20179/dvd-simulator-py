import time
import sys
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from os import listdir
from statistics import mean

import globalFuncs
from DVD_Screen import Menu
from Dvds import DVDS

#MAIN MENU
def VARS():
    global winWidth, winHeight, win

    pygame.display.set_caption("DVD")
    icos = pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in listdir("./src/ico_files")if "Menu" not in x and "FLess" not in x]))

    #DVDLogos setup
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in listdir("./DVD_Logos")]
    DVDSDict = {}

    #RANDOM VARS
    Run = True
    ADD = 1
    leaders = 0

    #color settings
    R, G, B = 0, 0, 0; baseColor = 255
    inverseRGBColor = (255 - R, 255 - G, 255 - B)

    #FONTS
    fonts = {
        "mainFont": pygame.font.SysFont("AR DESTINE", 25),
        "DVDInfoFont": pygame.font.SysFont("AR DESTINE", 20)
        }

    #options
    options = {
        "ShowLeader": True,
        "ShowAdd": True,
        "ShowTotal": True,
        "ShowAVG": True,
        "ShowRGB": True,
        "ShowSum": True,
        "CycleColors": False,
        "opsOnTop": True,
        "ShowFps": True
        }
    FPSCap = 120
    
    #sounds
    sounds = {"windows": pygame.mixer.Sound(r".\src\Sounds\WINXP_Startup.wav"), 
           "THX": pygame.mixer.Sound(r".\src\Sounds\THX_Sound.wav"), 
           "disney": pygame.mixer.Sound(r".\src\Sounds\Disney.wav"),
           "pixar": pygame.mixer.Sound(r".\src\Sounds\Pixar.wav"),
           "fox": pygame.mixer.Sound(r".\src\Sounds\Fox.wav"),
           "clap": pygame.mixer.Sound(r".\src\Sounds\Clap.wav")}

    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))


    return DVD_Logos, DVDSDict, Run ,ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap
def swap(winWidth, winHeight, SH, SW):
    pygame.display.quit()
    import Featureless
    Featureless.main(winWidth, winHeight, SH, SW)

def mainKeyChks(**kwargs):
    for varName, var in kwargs.items():
        if varName == "DVDSDict": DVDSDict = var
        if varName == "options": options = var
        if varName == "sounds": sounds = var
        if varName == "Run": Run = var
        if varName == "FPSCap": FPSCap = var

    keys = pygame.key.get_pressed()
    if keys[pygame.K_F5]: DVDSDict.clear()     
    if keys[pygame.K_F6]: options["CycleColors"] = True if not options["CycleColors"] else False
        
    if keys[pygame.K_F3]:
        for option in options:
            if option != "CycleColors": options[option] = True if not options[option] else False
    
    #options
    if keys[pygame.K_h]: options["ShowLeader"] = False if options["ShowLeader"] else True      
    if keys[pygame.K_t]: options["ShowTotal"] = False if options["ShowTotal"] else True      
    if keys[pygame.K_a]: options["ShowAdd"] = False if options["ShowAdd"] else True       
    if keys[pygame.K_m]: options["ShowAVG"] = False if options["ShowAVG"] else True       
    if keys[pygame.K_c]: options["ShowRGB"] = False if options["ShowRGB"] else True
    if keys[pygame.K_s]: options["ShowSum"] = False if options["ShowSum"] else True
    if keys[pygame.K_f]: options["ShowFps"] = False if options["ShowFps"] else True
    if keys[pygame.K_UP] or keys[pygame.K_DOWN]: options["opsOnTop"] = False if options["opsOnTop"] else True

    #FPS
    if keys[pygame.K_LSHIFT] and keys[pygame.K_UP]: FPSCap += 1 if not keys[pygame.K_LCTRL] else 10
    if keys[pygame.K_LSHIFT] and keys[pygame.K_DOWN]: FPSCap -= 1 if not keys[pygame.K_LCTRL] else 10

    #;)
    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]: sounds["windows"].play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]: sounds["THX"].play()   
    if keys[pygame.K_d] and keys[pygame.K_i] and keys[pygame.K_s]: sounds["disney"].play()
    if keys[pygame.K_p] and keys[pygame.K_i] and keys[pygame.K_x]: sounds["pixar"].play()
    if keys[pygame.K_f] and keys[pygame.K_o] and keys[pygame.K_x]: sounds["fox"].play()
    if keys[pygame.K_s] and keys[pygame.K_e] and keys[pygame.K_c] and keys[pygame.K_r] and keys[pygame.K_t]:
        pygame.display.quit()
        from Secret import main as m
        m(len(DVDSDict), SH, SW)

    #random facts
    if keys[pygame.K_d] and keys[pygame.K_LSHIFT]: globalFuncs.randDisMov()
    if keys[pygame.K_p] and keys[pygame.K_LSHIFT]: globalFuncs.randPixMov()

    #quitting/switching/main menu
    if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_F4]): Run = False; pygame.display.quit(); pygame.quit()
    if keys[pygame.K_F12]: swap(winWidth, winHeight, SH, SW)
    if keys[pygame.K_PAUSE]: 
        if keys[pygame.K_LSHIFT]: swap(winWidth, winHeight, SH, SW)           
        else:
            pygame.display.quit()
            Menu().mainMenu()

    if keys[pygame.K_F2]: pygame.image.save(win, f'SCREENSHOTS\{time.time()}.jpeg')

    return DVDSDict, options, sounds, Run, FPSCap

def mouseChks(**kwargs):
    for varName, var in kwargs.items():
        if varName == "ADD": ADD = var
        if varName == "DVDSDict": DVDSDict = var
        if varName == "R": R = var
        if varName == "G": G = var
        if varName == "B": B = var
        if varName == "baseColor": baseColor = var
        if varName == "event": event = var
        if varName == "DVD_Logos": DVD_Logos = var

    ADD = round(ADD)

    MPos, keys = pygame.mouse.get_pos(), pygame.key.get_pressed()

    if event.button == 1: #left click
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]:
            for DVD in DVDSDict:
                if MPos[0] > DVDSDict[DVD].SX and MPos[0] < DVDSDict[DVD].SX + DVDSDict[DVD].SW and MPos[1] > DVDSDict[DVD].SY and MPos[1] < DVDSDict[DVD].SY + DVDSDict[DVD].SH: DVDSDict[DVD].Move = False if DVDSDict[DVD].Move else True
        else:
            for a in range(ADD):
                DVDSDict[len(DVDSDict) + 1] = DVDS(winWidth, winHeight, DVD_Logos, SH, SW)
                if keys[pygame.K_LSHIFT]: DVDSDict[len(DVDSDict)].dispInfo = True

    elif event.button == 2: #middle click
        if keys[pygame.K_LSHIFT]:
            for plc, DVD in DVDSDict.items():
                if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH:
                    temp = DVDSDict[len(DVDSDict)]
                    DVDSDict[len(DVDSDict)] = DVDSDict[plc]
                    DVDSDict[plc] = temp
                    del DVDSDict[len(DVDSDict)]
                    break

        else:
            for a in range(ADD):
                if (length := len(DVDSDict)) >= 1: del DVDSDict[length]

    elif event.button == 3: #right click
        for DVD in DVDSDict.values():
            if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH:
                DVD.dispInfo = False if DVD.dispInfo else True
                break
        else:
            if keys[pygame.K_LCTRL]:
                for DVD in DVDSDict.values(): DVD.dispInfo  = False if DVD.dispInfo else True
            else:
                for a in range(ADD):
                    DVDSDict[len(DVDSDict) + 1] = DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1])
                    DVDSDict[len(DVDSDict)].dispInfo = True if keys[pygame.K_LSHIFT] else False
            
    elif event.button == 4: #Mouse wheel up
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]:
            MPos = pygame.mouse.get_pos()
            for DVD in DVDSDict.values():
                if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH: DVD.currentLogo = random.choice(DVD_Logos); break
                    
        elif keys[pygame.K_LCTRL]   and baseColor <= 255 - plus: baseColor += plus
            
        elif keys[pygame.K_r] and R <= 255 - plus: R += plus       
        elif keys[pygame.K_g] and G <= 255 - plus: G += plus
        elif keys[pygame.K_b] and B <= 255 - plus: B += plus
           
        else:
            ADD += plus

    elif event.button == 5: #mouse wheel down
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]:
            MPos = pygame.mouse.get_pos()
            for DVD in DVDSDict.values():
                if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH: DVD.currentLogo = random.choice(DVD_Logos); break

        elif keys[pygame.K_LCTRL]   and baseColor >= plus: baseColor -= plus

        elif R >= plus and keys[pygame.K_r]: R -= plus
        elif G >= plus and keys[pygame.K_g]: G -= plus          
        elif B >= plus and keys[pygame.K_b]: B -= plus

        elif ADD >= plus: ADD -= plus

    return ADD, DVDSDict, R, G, B, baseColor

def cycleColors(**kwargs):
    for varName, var in kwargs.items():
        if varName == "R": R = var
        if varName == "G": G = var
        if varName == "B": B = var
        if varName == "baseColor": baseColor = var
    if R != baseColor and G != baseColor and B != baseColor:
        R = baseColor
        G = 0
        B = 0

    if R == baseColor and G >= 0 and B == 0 and G < baseColor: G += 1    
    if R <= baseColor and G == baseColor and B == 0 and R > 0: R -= 1      
    if R == 0 and G == baseColor and B >= 0 and B < baseColor: B += 1 
    if R == 0 and G <= baseColor and B == baseColor and G > 0: G -= 1 
    if R >= 0 and G == 0 and B == baseColor and R < baseColor: R += 1
    if R == baseColor and G == 0 and B <= baseColor and B > 0: B -= 1
        
    return R, G, B, baseColor

def renderDVDS(**kwargs):
    for varName, var in kwargs.items():
        if varName == "fonts": fonts = var
        if varName == "DVDSDict": DVDSDict = var
        if varName == "inverseRGBColor": inverseRGBColor = var
        if varName == "win": win = var

    for DVD in DVDSDict.values():
        win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
        if DVD.dispInfo: win.blit(fonts["DVDInfoFont"].render(f'wall hits: {DVD.wallHits}', False, inverseRGBColor), (DVD.SX + DVD.SW, DVD.SY))

def main(vars):
    DVD_Logos, DVDSDict, Run ,ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap = vars
    DVDSDict[1] = DVDS(winWidth, winHeight, DVD_Logos, SH, SW)
    clock = pygame.time.Clock()

    while Run:
        clock.tick(FPSCap)
        for event in pygame.event.get(): #mouse clicks and button presses
            if event.type == pygame.QUIT: pygame.display.quit(); pygame.quit(); Run = False; break
            if event.type == pygame.KEYDOWN: DVDSDict, options, sounds, Run, FPSCap = mainKeyChks(DVDSDict=DVDSDict, options=options, sounds=sounds, Run=Run, win=win, FPSCap=FPSCap)  
            if event.type == pygame.MOUSEBUTTONDOWN: ADD, DVDSDict, R, G, B, baseColor = mouseChks(ADD=ADD, DVDSDict=DVDSDict, SH=SH, SW=SW, R=R, G=G, B=B, baseColor=baseColor, event=event, DVD_Logos=DVD_Logos, winWidth=winWidth, winHeight=winHeight)    
            
        else:
            if len(DVDSDict) >= 20:
                for DVD in DVDSDict.values():
                    if DVD.Move: break    
                else:
                    sounds["clap"].play()
                    for DVD in DVDSDict.values(): DVD.Move = True
                        
            inverseRGBColor = (255 - R, 255 - G, 255 - B)

            if options["CycleColors"]: R, G, B, baseColor = cycleColors(R=R, G=G, B=B, baseColor=baseColor)  
            
            #setting stats
            if hits := [x.wallHits for x in DVDSDict.values()]:
                leaders = max(hits)
                totalHits = sum(hits)
                AVGHits = mean(hits) if len(hits) >= 2 else totalHits

            #rendering
            for DVD in DVDSDict.values():
                if DVD.Move: DVD(winWidth,  winHeight, DVD_Logos)

            win.fill((R, G, B))
            rendSpot1, rendSpot2, rendSpot3, rendSpot4, rendSpot5, rendSpot6, rendSpot7, rendSpot8 = 0, 20, 40, 60, 80, 100, 120, 140
            if not options["opsOnTop"]:
                renderDVDS(fonts=fonts, DVDSDict=DVDSDict, inverseRGBColor=inverseRGBColor, win=win)

            if options["ShowFps"]: win.blit(fonts["DVDInfoFont"].render(f'FPS (f): {round(clock.get_fps(), 2)}', False, inverseRGBColor), (0, rendSpot1))
            if options["ShowAdd"]: win.blit(fonts["mainFont"].render(f'ADD (a): {ADD}', False, inverseRGBColor), (0, rendSpot2))
            if options["ShowTotal"]: win.blit(fonts["mainFont"].render(f'DVDS (t): {len(DVDSDict)}', False, inverseRGBColor), (0, rendSpot3))
            if options["ShowSum"]: win.blit(fonts["mainFont"].render(f'TOTAL HITS (s): {totalHits}', False, inverseRGBColor), (0, rendSpot4))
            if options["ShowLeader"]: leaderBoardDisp = win.blit(fonts["mainFont"].render(f'MOST HITS (h): {leaders}', False, inverseRGBColor), (0, rendSpot5))
            if options["ShowAVG"]: win.blit(fonts["DVDInfoFont"].render(f'AVG HITS (m): {AVGHits}', False, inverseRGBColor), (0, rendSpot8))
            if options["ShowRGB"]:
                win.blit(fonts["DVDInfoFont"].render(f'RGB (c): {R, G, B}', False, inverseRGBColor), (0, rendSpot6))
                win.blit(fonts["DVDInfoFont"].render(f'RGB Base: {baseColor}', False, inverseRGBColor), (0, rendSpot7))
            if options["opsOnTop"]: renderDVDS(fonts=fonts, DVDSDict=DVDSDict, inverseRGBColor=inverseRGBColor, win=win)
            
            pygame.display.update()

def mainInit(winwidth, winheight, sh, sw):
    global SH, SW, winWidth, winHeight; SH, SW = int(sh), int(sw)
    winWidth, winHeight = winwidth, winheight
    pygame.init(); pygame.mixer.init(); pygame.font.init()
    VAR = VARS()
    main(VAR)