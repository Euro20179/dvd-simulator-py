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

class Options:
    def __init__(self, on, key, name):
        self.on = on
        self.key = key
        self.name = name

    def switch(self, keys):
        if keys[self.key]: self.on = False if self.on else True

#MAIN MENU
def VARS():
    global winWidth, winHeight, win

    pygame.display.set_caption("DVD")
    icos = pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in listdir("./src/ico_files")if "Menu" not in x and "FLess" not in x]))

    #DVDLogos setup
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in listdir("./DVD_Logos")]
    DVDSList = []

    #RANDOM VARS
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
    options = [Options(True, pygame.K_h, "ShowLeader"), 
               Options(True, pygame.K_a, "ShowAdd"),
               Options(True, pygame.K_t, "ShowTotal"),
               Options(True, pygame.K_c, "ShowRGB"),
               Options(True, pygame.K_s, "ShowSum"),
               Options(False,  pygame.K_F6, "CycleColors"),
               Options(True, pygame.K_UP, "opsOnTop"),
               Options(True, pygame.K_f, "ShowFps"),
               Options(False, pygame.K_p, "ShowAVGPos"),
               Options(True, pygame.K_m, "ShowAVG")]

    FPSCap = 120

    #sounds
    sounds = {"windows": pygame.mixer.Sound(r".\src\Sounds\WINXP_Startup.wav"), 
           "THX": pygame.mixer.Sound(r".\src\Sounds\THX_Sound.wav"), 
           "disney": pygame.mixer.Sound(r".\src\Sounds\Disney.wav"),
           "pixar": pygame.mixer.Sound(r".\src\Sounds\Pixar.wav"),
           "fox": pygame.mixer.Sound(r".\src\Sounds\Fox.wav"),
           "clap": pygame.mixer.Sound(r".\src\Sounds\Clap.wav")}

    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))


    return DVD_Logos, DVDSList, ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap
def swap(winWidth, winHeight, SH, SW):
    pygame.display.quit()
    import Featureless
    Featureless.main(winWidth, winHeight, SH, SW)

def mouseCollide(MPos, DVD):
    return True if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH else False

def mainKeyChks(*args):
    DVDSList, options, sounds, Run, win = args

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_F3]:
        for op in options:
            if op.name != "CycleColors" and op.name != "ShowAVGPos":
                op.on = False if op.on else True
    
    #options
    for op in options: op.switch(keys)

    if keys[pygame.K_F5]: DVDSList.clear()

    #;)
    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]: sounds["windows"].play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]: sounds["THX"].play()   
    if keys[pygame.K_d] and keys[pygame.K_i] and keys[pygame.K_s]: sounds["disney"].play()
    if keys[pygame.K_p] and keys[pygame.K_i] and keys[pygame.K_x]: sounds["pixar"].play()
    if keys[pygame.K_f] and keys[pygame.K_o] and keys[pygame.K_x]: sounds["fox"].play()
    if keys[pygame.K_s] and keys[pygame.K_e] and keys[pygame.K_c] and keys[pygame.K_r] and keys[pygame.K_t] or keys[pygame.K_F10]:
        pygame.display.quit()
        from Secret import main as m
        m(len(DVDSList), SH, SW, winWidth, winHeight)

    #random facts
    if keys[pygame.K_d] and keys[pygame.K_LSHIFT]: globalFuncs.randDisMov()
    if keys[pygame.K_p] and keys[pygame.K_LSHIFT]: globalFuncs.randPixMov()

    #quitting/switching/main menu
    if keys[pygame.K_F12]: swap(winWidth, winHeight, SH, SW)
    if keys[pygame.K_PAUSE]: 
        if keys[pygame.K_LSHIFT]: swap(winWidth, winHeight, SH, SW)           
        else:
            pygame.display.quit()
            Menu().mainMenu()

    if keys[pygame.K_F2]: pygame.image.save(win, f'SCREENSHOTS\{time.time()}.jpeg')

    return DVDSList, options, sounds, Run

def mouseChks(*args):
    options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos = args

    ADD = round(ADD)

    MPos, keys = pygame.mouse.get_pos(), pygame.key.get_pressed()

    if event.button == 1: #left click
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]: #Freeze DVD at mouse
            
            for DVD in DVDSList:
                if mouseCollide(MPos, DVD): DVD.Move = False if DVD.Move else True
        else:
            for a in range(ADD): #add DVDS randomly
                DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW))
                if keys[pygame.K_LSHIFT]: DVDSList[-1].dispInfo = True

    elif event.button == 2: #middle click
        if keys[pygame.K_LSHIFT]: #remove DVD at mouse
            for plc, DVD in enumerate(DVDSList): DVDSList.pop(plc) if mouseCollide(MPos, DVD) else None

        else:
            for a in range(ADD): #remove DVDS
                if (length := len(DVDSList)) >= 1: DVDSList.pop(-1)

    elif event.button == 3: #right click
        for DVD in DVDSList: #DVD show info
            if mouseCollide(MPos, DVD):
                DVD.dispInfo = False if DVD.dispInfo else True
                break

        else:
            if MPos[0] > AVGX and MPos[0] < AVGX + SW and MPos[1] > AVGY and MPos[1] < AVGY + SH: avgPosDVD.dispInfo = True if not avgPosDVD.dispInfo else False #avg DVD show info
            elif keys[pygame.K_LCTRL]: #all DVD show info
                for DVD in DVDSList: DVD.dispInfo = False if DVD.dispInfo else True
            else: #add DVDS
                for a in range(ADD): DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1], dispInfo=True if keys[pygame.K_LSHIFT] else False))
                    
            
    elif event.button == 4: #Mouse wheel up
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]: #change DVD logo at mouse
            for DVD in DVDSList: DVD.currentLogo = random.choice(DVD_Logos) if mouseCollide(MPos, DVD) else DVD.currentLogo
                    
        elif keys[pygame.K_LCTRL] and baseColor <= 255 - plus: baseColor += plus
            
        elif keys[pygame.K_r] and R <= 255 - plus: R += plus       
        elif keys[pygame.K_g] and G <= 255 - plus: G += plus
        elif keys[pygame.K_b] and B <= 255 - plus: B += plus
           
        else:
            ADD += plus

    elif event.button == 5: #mouse wheel down
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]: #change DVD logo at mouse
            for DVD in DVDSList: DVD.currentLogo = random.choice(DVD_Logos) if mouseCollide(MPos, DVD) else DVD.currentLogo

        elif keys[pygame.K_LCTRL] and baseColor >= plus: baseColor -= plus

        elif R >= plus and keys[pygame.K_r]: R -= plus
        elif G >= plus and keys[pygame.K_g]: G -= plus          
        elif B >= plus and keys[pygame.K_b]: B -= plus

        elif ADD >= plus: ADD -= plus

    return ADD, DVDSList, R, G, B, baseColor

def cycleColors(*args):
    R, G, B, baseColor = args

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

def renderDVDS(*args):
    fonts, DVDSList, inverseRGBColor, win = args

    for DVD in DVDSList:
        win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
        if DVD.dispInfo: 
            win.blit(fonts["DVDInfoFont"].render(f'wall hits: {DVD.wallHits}', False, inverseRGBColor), (DVD.SX + DVD.SW, DVD.SY))
            win.blit(fonts["DVDInfoFont"].render(f'X, Y: {round(DVD.SX, 2), round(DVD.SY, 2)}', False, inverseRGBColor), (DVD.SX + DVD.SW, DVD.SY + 20))

def main(vars):
    global AVGX, AVGY, avgPosDVD

    DVD_Logos, DVDSList, ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap = vars
    DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW))

    AVGX, AVGY = mean([x.SX for x in DVDSList]), mean([y.SY for y in DVDSList])
    avgPosDVD = DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=AVGX, SY=AVGY)
    clock = pygame.time.Clock()

    while (Run := True):
        clock.tick(FPSCap)
        for event in pygame.event.get(): #mouse clicks and button presses
            if event.type == pygame.QUIT: pygame.quit(); Run = False; break
            if event.type == pygame.KEYDOWN: DVDSList, options, sounds, Run = mainKeyChks(DVDSList, options, sounds, Run, win)  
            if event.type == pygame.MOUSEBUTTONDOWN: ADD, DVDSList, R, G, B, baseColor = mouseChks(options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos)    
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and keys[pygame.K_LSHIFT]: FPSCap += 1
            if keys[pygame.K_DOWN] and keys[pygame.K_LSHIFT]: FPSCap -= 1
            if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.quit(); Run = False; break

            if len(DVDSList) >= 20:
                for DVD in DVDSList:
                    if DVD.Move: break    
                else:
                    sounds["clap"].play()
                    for DVD in DVDSList: DVD.Move = True

            if len(DVDSList) >= 1: AVGX, AVGY = mean([x.SX for x in DVDSList]), mean([y.SY for y in DVDSList])
                        
            inverseRGBColor = (255 - R, 255 - G, 255 - B)
            for op in options:
                if op.name == "CycleColors" and op.on: R, G, B, baseColor = cycleColors(R, G, B, baseColor)
            
            #setting stats
            if hits := [x.wallHits for x in DVDSList]:
                leaders, totalHits = max(hits), sum(hits)
                AVGHits = mean(hits) if len(hits) >= 2 else totalHits

            #rendering
            for DVD in DVDSList: DVD(winWidth, winHeight, DVD_Logos) if DVD.Move else None

            win.fill((R, G, B))
            #to make y position fiddling easier
            rendSpot1, rendSpot2, rendSpot3, rendSpot4, rendSpot5, rendSpot6, rendSpot7, rendSpot8 = 0, 20, 40, 60, 80, 100, 120, 140

            #options rendering
            for op in options:
                if op.name == "opsOnTop" and not op.on: renderDVDS(fonts, DVDSList, inverseRGBColor, win)
                if op.on:
                    if op.name == "ShowFps": win.blit(fonts["DVDInfoFont"].render(f'FPS (f): {round(clock.get_fps(), 2)}', False, inverseRGBColor), (0, rendSpot1))
                    if op.name == "ShowAdd": win.blit(fonts["mainFont"].render(f'ADD (a): {ADD}', False, inverseRGBColor), (0, rendSpot2))
                    if op.name == "ShowTotal": win.blit(fonts["mainFont"].render(f'DVDS (t): {len(DVDSList)}', False, inverseRGBColor), (0, rendSpot3))
                    if op.name == "ShowSum": win.blit(fonts["mainFont"].render(f'TOTAL HITS (s): {totalHits}', False, inverseRGBColor), (0, rendSpot4))
                    if op.name == "ShowLeader": leaderBoardDisp = win.blit(fonts["mainFont"].render(f'MOST HITS (h): {leaders}', False, inverseRGBColor), (0, rendSpot5))
                    if op.name == "ShowAVG": win.blit(fonts["DVDInfoFont"].render(f'AVG HITS (m): {AVGHits}', False, inverseRGBColor), (0, rendSpot8))
                    if op.name == "ShowAVGPos" and len(DVDSList) >= 1:
                        win.blit(avgPosDVD.currentLogo, (AVGX, AVGY))
                        if avgPosDVD.dispInfo: win.blit(fonts["DVDInfoFont"].render(f'X, Y: ({round(AVGX, 2), round(AVGY, 2)})', False, inverseRGBColor), (AVGX + SW, AVGY))
                    if op.name == "ShowRGB":
                        win.blit(fonts["DVDInfoFont"].render(f'RGB (c): {R, G, B}', False, inverseRGBColor), (0, rendSpot6))
                        win.blit(fonts["DVDInfoFont"].render(f'RGB Base: {baseColor}', False, inverseRGBColor), (0, rendSpot7))
                    if op.name == "opsOnTop": renderDVDS(fonts, DVDSList, inverseRGBColor, win)
            
            pygame.display.update()
            
def mainInit(winwidth, winheight, sh, sw):
    global SH, SW, winWidth, winHeight
    SH, SW = int(sh), int(sw)
    winWidth, winHeight = winwidth, winheight
    pygame.init(); pygame.mixer.init(); pygame.font.init()
    main(VARS())