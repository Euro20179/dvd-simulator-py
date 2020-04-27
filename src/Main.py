import time
import sys
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import os
from os import listdir
from statistics import mean

import globalFuncs
from DVD_Screen import Menu
from classes import DVDS, Options



#MAIN MENU
def VARS():
    global winWidth, winHeight, win, frame

    frame = 0

    pygame.display.set_caption("DVD")
    icos = pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in listdir("./src/ico_files")if "Menu" not in x and "FLess" not in x]))

    #DVDLogos setup
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in listdir("./DVD_Logos")]
    DW, DH = DVD_Logos[0].get_size()
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
    options = [Options(True, pygame.K_h, "ShowLeader", 0, 80),
               Options(True, pygame.K_a, "ShowAdd", 0, 20),
               Options(True, pygame.K_t, "ShowTotal", 0, 40),
               Options(True, pygame.K_c, "ShowRGB", 0, 100),
               Options(True, pygame.K_b, "ShowRGBBase", 0, 120),
               Options(True, pygame.K_s, "ShowSum", 0, 60),
               Options(False,  pygame.K_F6, "CycleColors", 0, None),
               Options(True, pygame.K_UP, "opsOnTop", 0, None),
               Options(True, pygame.K_f, "ShowFps", 0, 0),
               Options(False, pygame.K_p, "ShowAVGPos", 0, None),
               Options(True, pygame.K_m, "ShowAVG", 0, 140)]

    FPSCap = 120

    #sounds
    sounds = {"windows": pygame.mixer.Sound(r".\src\Sounds\WINXP_Startup.wav"), 
           "THX": pygame.mixer.Sound(r".\src\Sounds\THX_Sound.wav"), 
           "disney": pygame.mixer.Sound(r".\src\Sounds\Disney.wav"),
           "pixar": pygame.mixer.Sound(r".\src\Sounds\Pixar.wav"),
           "fox": pygame.mixer.Sound(r".\src\Sounds\Fox.wav"),
           "clap": pygame.mixer.Sound(r".\src\Sounds\Clap.wav")}

    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)


    return DVD_Logos, DVDSList, ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap, DW, DH
def swap(winWidth, winHeight, SH, SW):
    pygame.display.quit()
    import Featureless
    Featureless.main(winWidth, winHeight, SH, SW)

def mouseCollide(MPos, DVD):
    return True if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH else False

def recolorInverseDVDS(*args):
    DVDSList, inverseRGBColor, DVD_Logos, DW, DH = args
    r, g, b = inverseRGBColor
    s = DVD_Logos[0].copy()
    s.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    s.fill(inverseRGBColor + (0,), None, pygame.BLEND_RGBA_MAX)
    DVD_Logos.pop(-1)
    DVD_Logos.insert(-1, s)
    for n, DVD in enumerate(DVDSList):
        if DVD.inverseColor:
            DVD.currentLogo = DVD_Logos[-1]

    return DVDSList, DVD_Logos


def mainKeyChks(*args):
    DVDSList, options, sounds, Run, win, ADD, DVD_Logos = args

    keys = pygame.key.get_pressed()

    if keys[pygame.K_F3]:
        for op in options:
            if op.name != "CycleColors" and op.name != "ShowAVGPos":
                op.on = False if op.on else True
    
    #options
    for op in options: op.switch(keys)

    if keys[pygame.K_SPACE]:
        for DVD in DVDSList:
            DVD.Move = False if DVD.Move else True

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

    if keys[pygame.K_F11]: 
        flags = win.get_flags()
        pygame.display.set_mode((winWidth, winHeight),flags^pygame.FULLSCREEN)

    if keys[pygame.K_F2]: pygame.image.save(win, f'SCREENSHOTS\{time.time()}.jpeg')

    return DVDSList, options, sounds, Run

def mouseChks(*args):
    options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos = args

    ADD = round(ADD)

    MPos = pygame.mouse.get_pos(); keys = pygame.key.get_pressed()

    if event.button == 1: #left click

        if keys[pygame.K_LALT]:
            for x in range(ADD):
                DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, "inverseColor"))

        elif keys[pygame.K_LCTRL]: #Freeze DVD at mouse
            
            for DVD in DVDSList:
                if mouseCollide(MPos, DVD): DVD.Move = False if DVD.Move else True

        else:
            for a in range(ADD): #add DVDS randomly
                DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW))
                if keys[pygame.K_LSHIFT]: DVDSList[-1].dispInfo = True

    elif event.button == 2: #middle click
        if keys[pygame.K_LSHIFT]: #remove DVD at mouse
            for plc, DVD in enumerate(DVDSList): 
                if mouseCollide(MPos, DVD): DVDSList.pop(plc)

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
            
            elif keys[pygame.K_LALT]:
                for x in range(ADD):
                    DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, "inverseColor", SX=MPos[0], SY=MPos[1], dispInfo=True if keys[pygame.K_LSHIFT] else False))

            elif keys[pygame.K_LCTRL]: #all DVD show info
                for DVD in DVDSList: DVD.dispInfo = False if DVD.dispInfo else True
            else: #add DVDS
                for a in range(ADD): DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1], dispInfo=True if keys[pygame.K_LSHIFT] else False))
                    
            
    elif event.button == 4: #Mouse wheel up
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]: #change DVD logo at mouse
            for DVD in DVDSList: DVD.currentLogo = random.choice(DVD_Logos) if mouseCollide(MPos, DVD) else DVD.currentLogo
                    
        if keys[pygame.K_LCTRL] and baseColor <= 255 - plus: baseColor += plus
            
        elif keys[pygame.K_r] and R <= 255 - plus: R += plus       
        elif keys[pygame.K_g] and G <= 255 - plus: G += plus
        elif keys[pygame.K_b] and B <= 255 - plus: B += plus
           
        else:
            ADD += plus

    elif event.button == 5: #mouse wheel down
        plus = 10 if keys[pygame.K_LSHIFT] else 1
        if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL]: #change DVD logo at mouse
            for DVD in DVDSList: DVD.currentLogo = random.choice(DVD_Logos) if mouseCollide(MPos, DVD) else DVD.currentLogo

        #rgb background stuff
        if keys[pygame.K_LCTRL] and baseColor >= plus: baseColor -= plus

        elif R >= plus and keys[pygame.K_r]: R -= plus
        elif G >= plus and keys[pygame.K_g]: G -= plus          
        elif B >= plus and keys[pygame.K_b]: B -= plus

        elif ADD >= plus: ADD -= plus

    return ADD, DVDSList, R, G, B, baseColor

def cycleColors(*args): #cycles the background color
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

def renderDVDS(*args): #see function name
    fonts, DVDSList, inverseRGBColor, win = args

    for DVD in DVDSList:
        win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
        if DVD.dispInfo: 
            win.blit(fonts["DVDInfoFont"].render(f'wall hits: {DVD.wallHits}', False, inverseRGBColor), (DVD.SX + DVD.SW, DVD.SY))
            win.blit(fonts["DVDInfoFont"].render(f'X, Y: {round(DVD.SX, 2), round(DVD.SY, 2)}', False, inverseRGBColor), (DVD.SX + DVD.SW, DVD.SY + 20))

def blitOps(*args):
    fonts, font, string, color, renderSpot = args
    win.blit(fonts[font].render(string, True, color), (0, renderSpot))

def main(vars):
    global AVGX, AVGY, avgPosDVD, winWidth, winHeight, frame

    frame += 1

    DVD_Logos, DVDSList, ADD, leaders, R, G, B, baseColor, inverseRGBColor, fonts, options, sounds, FPSCap, DW, DH = vars
    DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW))

    AVGX, AVGY = mean([x.SX for x in DVDSList]), mean([y.SY for y in DVDSList])
    avgPosDVD = DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=AVGX, SY=AVGY)
    clock = pygame.time.Clock()

    while (Run := True):
        clock.tick(FPSCap)
        for event in pygame.event.get(): #mouse clicks and button presses
            if event.type == pygame.QUIT: pygame.quit(); Run = False; break
            if event.type == pygame.KEYDOWN: DVDSList, options, sounds, Run = mainKeyChks(DVDSList, options, sounds, Run, win, ADD, DVD_Logos)  
            if event.type == pygame.MOUSEBUTTONDOWN: ADD, DVDSList, R, G, B, baseColor = mouseChks(options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos)    
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                winWidth, winHeight = pygame.display.get_surface().get_size()
        else: #key checks
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and keys[pygame.K_LSHIFT]: FPSCap += 1
            if keys[pygame.K_DOWN] and keys[pygame.K_LSHIFT]: FPSCap -= 1
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                Menu().mainMenu()
            if keys[pygame.K_PAUSE]:    
                pygame.quit()
                Menu().mainMenu()
            elif (keys[pygame.K_ESCAPE] and keys[pygame.K_LSHIFT]) or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.quit(); Run = False; break


            if len(DVDSList) >= 20: #checks if you stopped all dvds with 20+ dvds on screen
                for DVD in DVDSList:
                    if DVD.Move: break    
                else:
                    sounds["clap"].play()
                    for DVD in DVDSList: DVD.Move = True

            if len(DVDSList) > 1: AVGX, AVGY = mean([x.SX for x in DVDSList]), mean([y.SY for y in DVDSList]) #sets avgx, avgy
                        
            inverseRGBColor = (255 - R, 255 - G, 255 - B) #sets inverse color

            if options[6].on: R, G, B, baseColor = cycleColors(R, G, B, baseColor)
            
            #setting stats
            if hits := [x.wallHits for x in DVDSList]:
                leaders, totalHits = max(hits), sum(hits)
                AVGHits = mean(hits) if len(hits) >= 2 else totalHits

            #rendering
            DVDSList, DVD_Logos = recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos, DW, DH)
            for DVD in DVDSList: 
                if DVD.Move: DVD(winWidth, winHeight, DVD_Logos)

            win.fill((R, G, B))
            
            #options rendering
            for op in options:
                if op.name == "opsOnTop" and not op.on: renderDVDS(fonts, DVDSList, inverseRGBColor, win)
                if op.on:
                    if op.name == "ShowFps": blitOps(fonts, "DVDInfoFont", f'FPS (f): {round(clock.get_fps(), 2)}', inverseRGBColor, op.yRend)
                    if op.name == "ShowAdd": blitOps(fonts, "mainFont", f'ADD (a): {ADD}', inverseRGBColor, op.yRend)
                    if op.name == "ShowTotal": blitOps(fonts, "mainFont", f'DVDS (t): {len(DVDSList)}', inverseRGBColor, op.yRend)
                    if op.name == "ShowSum": blitOps(fonts, "mainFont", f'TOTAL HITS (s): {totalHits}', inverseRGBColor, op.yRend)
                    if op.name == "ShowLeader": blitOps(fonts, "mainFont", f'MOST HITS (h): {leaders}', inverseRGBColor, op.yRend)
                    if op.name == "ShowAVG": blitOps(fonts, "DVDInfoFont", f'AVG HITS (m): {AVGHits}', inverseRGBColor, op.yRend)
                    if op.name == "ShowAVGPos" and len(DVDSList) > 1:
                        win.blit(avgPosDVD.currentLogo, (AVGX, AVGY))
                        if avgPosDVD.dispInfo: win.blit(fonts["DVDInfoFont"].render(f'X, Y: ({round(AVGX, 2), round(AVGY, 2)})', False, inverseRGBColor), (AVGX + SW, AVGY))
                    if op.name == "ShowRGB": blitOps(fonts, "DVDInfoFont", f'RGB (c): {R, G, B}', inverseRGBColor, op.yRend)
                    if op.name == "ShowRGBBase": blitOps(fonts, "DVDInfoFont", f'RGB Base(b): {baseColor}', inverseRGBColor, op.yRend)
                    if op.name == "opsOnTop": renderDVDS(fonts, DVDSList, inverseRGBColor, win)
            
            pygame.display.update()
            
def mainInit(winwidth, winheight, sh, sw):
    global SH, SW, winWidth, winHeight

    SH, SW = int(sh), int(sw)
    winWidth, winHeight = winwidth, winheight
    pygame.init(); pygame.mixer.init(); pygame.font.init()
    main(VARS())