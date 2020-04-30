import datetime
import random
import pygame
import tkinter as tk
import os
import wikipedia
import webbrowser
import bs4 as bs
import requests
import playsound
import pandas as pd
from tkinter import messagebox
from statistics import mean

from DVD_Screen import Menu
from src.classes import *

#goes from this mode to featureless
def swap(winWidth, winHeight, SH, SW):
    pygame.display.quit()
    import src.Featureless as Featureless
    Featureless.main(winWidth, winHeight, SH, SW)

#checks if mouse is clicking on dvd
def mouseCollide(MPos, DVD):
    return True if MPos[0] > DVD.SX and MPos[0] < DVD.SX + DVD.SW and MPos[1] > DVD.SY and MPos[1] < DVD.SY + DVD.SH else False

#main key checks
def mainKeyChks(*args):
    DVDSList, options, sounds, Run, win = args

    keys = pygame.key.get_pressed()

    #toggles all options
    if keys[pygame.K_F3]:
        if Options.On:
            for op in options.values():
                if type(op) is not VisualOptions:
                    op.setOn(False)
            Options.setClsOn(False)
        else:
            for op in options.values():
                if type(op) is not VisualOptions:
                    op.setOn(True)
            Options.setClsOn(True)
    
    #options
    for op in options.values(): 
        op.switch(keys)
        
    #stops all logos
    if keys[pygame.K_SPACE]:
        if DVDSList[0].Move:        
           for DVD in DVDSList:
               DVD.setMove(False)
        else:
            for DVD in DVDSList:
                DVD.setMove(True)

    #clears all logos
    if keys[pygame.K_F5]: DVDSList.clear()

    #;)
    if keys[pygame.K_w] and keys[pygame.K_i] and keys[pygame.K_n]: sounds["windows"].play()
    if keys[pygame.K_t] and keys[pygame.K_h] and keys[pygame.K_x]: sounds["THX"].play()   
    if keys[pygame.K_d] and keys[pygame.K_i] and keys[pygame.K_s]: sounds["disney"].play()
    if keys[pygame.K_p] and keys[pygame.K_i] and keys[pygame.K_x]: sounds["pixar"].play()
    if keys[pygame.K_f] and keys[pygame.K_o] and keys[pygame.K_x]: sounds["fox"].play()
    if keys[pygame.K_e] and keys[pygame.K_r] and keys[pygame.K_o]:
        pygame.quit()
        playsound.playsound(r".\src\Sounds\error.wav")
        Menu().mainMenu()

    if keys[pygame.K_s] and keys[pygame.K_e] and keys[pygame.K_c] and keys[pygame.K_r] and keys[pygame.K_t] or keys[pygame.K_F10]:
        pygame.display.quit()
        from src.Secret import main as m
        m(len(DVDSList), SH, SW, winWidth, winHeight)

    #quitting/switching/main menu
    if keys[pygame.K_F12]: swap(winWidth, winHeight, SH, SW)

    if keys[pygame.K_F11]: 
        flags = win.get_flags()
        pygame.display.set_mode((winWidth, winHeight),flags^pygame.FULLSCREEN)

    if keys[pygame.K_F2]: pygame.image.save(win, 'SCREENSHOTS\\{:%Y-%m-%d %H-%M-%S}.jpeg'.format(datetime.datetime.now()))

    #logo options
    if keys[pygame.K_9]:
        for DVD in DVDSList:
            DVD.setDispHits()
    if keys[pygame.K_0]:
        for DVD in DVDSList:
            DVD.setDispXY()
    if keys[pygame.K_MINUS]:
        for DVD in DVDSList:
            DVD.setDispXSpeed()
    if keys[pygame.K_EQUALS]:
        for DVD in DVDSList:
            DVD.setDispYSpeed()    

    #average pos dvd options
    if keys[pygame.K_z]:
        avgPosDVD.setDispXY()
    if keys[pygame.K_x]:
        avgPosDVD.setDispXYDist()

    return DVDSList, options, sounds, Run

#clicks
def mouseChks(*args):
    options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos, inverseRGBColor = args

    ADD = round(ADD)

    MPos = pygame.mouse.get_pos(); keys = pygame.key.get_pressed() #gets the mouse position, and keys pressed

    if event.button == 1: #left click
        for DVD in DVDSList:
            if mouseCollide(MPos, DVD): 
                DVD.setMove()
                return ADD, DVDSList, R, G, B, baseColor
        if mouseCollide(MPos, avgPosDVD):
            avgPosDVD.setMove()
            return ADD, DVDSList, R, G, B, baseColor

        if pygame.Rect(options["ShowLeader"].xRend, options["ShowLeader"].yRend, 100, 20).collidepoint(MPos):
            maxHits = max([x.wallHits for x in DVDSList])
            for DVD in DVDSList:
                if DVD.wallHits == maxHits:
                    pygame.mouse.set_pos(DVD.SX, DVD.SY)
                    DVD.setMove(False)

        elif keys[pygame.K_LALT]:
            for _ in range(ADD):
                if keys[pygame.K_LSHIFT]:
                    DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW, dispInfo=[True] * 4))
                    DVDSList[-1].recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos)
                else:
                    DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW))
                    DVDSList[-1].recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos)

        elif keys[pygame.K_LCTRL]:
            for _ in range(ADD):
                DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW))

        else:
            for _ in range(ADD): #add DVDS randomly
                if keys[pygame.K_LSHIFT]: 
                    DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, dispInfo=[True] * 4))
                else:
                    DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW))

    elif event.button == 2: #middle click
        if keys[pygame.K_LALT]:
            if keys[pygame.K_LSHIFT]:
                for DVD in DVDSList:
                    DVD.setSX((winWidth / 2) - SW)
                    DVD.setSY((winHeight / 2) - SH)
            else:
                for DVD in DVDSList:
                    DVD.setSX(avgPosDVD.SX)
                    DVD.setSY(avgPosDVD.SY)

        elif keys[pygame.K_LSHIFT]: #remove DVD at mouse
            for plc, DVD in enumerate(DVDSList): 
                if mouseCollide(MPos, DVD): DVDSList.pop(plc)
                

        else:
            for _ in range(ADD): #remove DVDS
                if len(DVDSList) >= 1: DVDSList.pop(-1)

    elif event.button == 3: #right click
        for DVD in DVDSList: #DVD show info
            if mouseCollide(MPos, DVD):
                if DVD.dispInfo:
                    DVD.setDispHits(False)
                    DVD.setDispXY(False)
                    DVD.setDispXSpeed(False)
                    DVD.setDispYSpeed(False)
                    DVD.setDispInfo(False)
                else:
                    DVD.setDispHits(True)
                    DVD.setDispXY(True)
                    DVD.setDispXSpeed(True)
                    DVD.setDispYSpeed(True)
                    DVD.setDispInfo(True)
                break

        else:
            if mouseCollide(MPos, avgPosDVD): 
                if avgPosDVD.dispInfo:
                    avgPosDVD.setDispInfo(False)
                    avgPosDVD.setDispXY(False)
                    avgPosDVD.setDispXYDist(False)
                else:
                    avgPosDVD.setDispInfo(True)
                    avgPosDVD.setDispXY(True)
                    avgPosDVD.setDispXYDist(True)#avg DVD show info
            
            elif keys[pygame.K_LALT]:
                for _ in range(ADD):
                    if keys[pygame.K_LSHIFT]:
                        DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1], dispInfo=[True] * 4))
                        DVDSList[-1].recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos)
                    else:
                        DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1]))
                        DVDSList[-1].recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos)

            elif keys[pygame.K_LCTRL]: #all DVD show info
                if DVD.dispInfo:
                    for DVD in DVDSList:
                        DVD.setDispHits(False)
                        DVD.setDispXY(False)
                        DVD.setDispXSpeed(False)
                        DVD.setDispYSpeed(False)
                        DVD.setDispInfo(False)
                else:
                    for DVD in DVDSList:
                        DVD.setDispHits(True)
                        DVD.setDispXY(True)
                        DVD.setDispXSpeed(True)
                        DVD.setDispYSpeed(True)
                        DVD.setDispInfo(True)

            else: #add DVDS
                for _ in range(ADD): 
                    if keys[pygame.K_LSHIFT]:
                        DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1], dispInfo=[True] * 4))
                    else:
                        DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, SH, SW, SX=MPos[0], SY=MPos[1]))
                    
            
    elif event.button == 4: #Mouse wheel up
        plus = 10 if keys[pygame.K_LSHIFT] else 1
      
        for DVD in DVDSList:
            if mouseCollide(MPos, DVD):
                if keys[pygame.K_LCTRL]:
                    sx = DVD.SX
                    sy = DVD.SY
                    DVDSList.remove(DVD)
                    DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW, SX=sx, SY=sy))
                else:
                    DVD.setLogo()
                    break
        else:
            if keys[pygame.K_LCTRL] and baseColor <= 255 - plus: baseColor += plus
                
            elif keys[pygame.K_r] and R <= 255 - plus: R += plus       
            elif keys[pygame.K_g] and G <= 255 - plus: G += plus
            elif keys[pygame.K_b] and B <= 255 - plus: B += plus
            
            else:
                ADD += plus

    elif event.button == 5: #mouse wheel down
        plus = 10 if keys[pygame.K_LSHIFT] else 1

        for DVD in DVDSList:
            if mouseCollide(MPos, DVD):
                if keys[pygame.K_LCTRL]:
                    sx = DVD.SX
                    sy = DVD.SY
                    DVDSList.remove(DVD)
                    DVDSList.append(InverseColorDVD(winWidth, winHeight, DVD_Logos, SH, SW, SX=sx, SY=sy))
                else:
                    DVD.setLogo()
                    break

        else:
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
        highest = max((R, G, B))
        if R == highest:
            R = baseColor
            B=G=0
        elif B == highest:
            B = baseColor
            R=G=0
        elif G == highest:
            G = baseColor
            R=B=0

    if R == baseColor and G >= 0 and B == 0 and G < baseColor: G += 1    
    if R <= baseColor and G == baseColor and B == 0 and R > 0: R -= 1      
    if R == 0 and G == baseColor and B >= 0 and B < baseColor: B += 1 
    if R == 0 and G <= baseColor and B == baseColor and G > 0: G -= 1 
    if R >= 0 and G == 0 and B == baseColor and R < baseColor: R += 1
    if R == baseColor and G == 0 and B <= baseColor and B > 0: B -= 1
        
    return R, G, B, baseColor

def blitOps(*args):
    fonts, font, string, color, x, renderSpot = args
    win.blit(fonts[font].render(string, True, color), (x, renderSpot))

def renderDVDS(*args): #see function name
    fonts, DVDSList, inverseRGBColor, win, options = args
    if options["ShowAVGPos"].on and len(DVDSList) > 1:
        win.blit(avgPosDVD.currentLogo, (avgPosDVD.SX, avgPosDVD.SY))
        if avgPosDVD.dispXY: 
            blitOps(fonts, "DVDInfoFont", f'X, Y: {round(avgPosDVD.SX, 2), round(avgPosDVD.SY, 2)} (z)', inverseRGBColor, avgPosDVD.SX + SW, avgPosDVD.SY)
        if avgPosDVD.dispXYDist:
            blitOps(fonts, "DVDInfoFont", f'X-mid, Y-mid: {round(avgPosDVD.SX - (winWidth / 2)), round(avgPosDVD.SY - (winHeight / 2))} (x)', inverseRGBColor, avgPosDVD.SX + SW, avgPosDVD.SY + 15)
    for DVD in DVDSList:
        win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
        if DVD.dispHits:
            blitOps(fonts, "DVDInfoFont", f'wall hits: {DVD.wallHits} (9)', inverseRGBColor, DVD.SX + DVD.SW, DVD.SY - 15)
        if DVD.dispXY:
            blitOps(fonts, "DVDInfoFont", f'X, Y: {round(DVD.SX, 2), round(DVD.SY, 2)} (0)', inverseRGBColor, DVD.SX + DVD.SW, DVD.SY)
        if DVD.dispXSpeed:
            blitOps(fonts, "DVDInfoFont", f'X Speed: {round(DVD.SXGain, 5)} (-)', inverseRGBColor, DVD.SX + DVD.SW, DVD.SY + 15)
        if DVD.dispYSpeed:
            blitOps(fonts, "DVDInfoFont", f'Y Speed: {round(DVD.SYGain, 5)} (=)', inverseRGBColor, DVD.SX + DVD.SW, DVD.SY + 30)


def main():
    global avgPosDVD, winWidth, winHeight, win

    pygame.display.set_caption("DVD")
    pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in os.listdir("./src/ico_files")if "Menu" not in x and "FLess" not in x]))
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)

    #DVDLogos setup
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in os.listdir("./DVD_Logos")]
    DVDSList = [DVDS(winWidth, winHeight, DVD_Logos, SH, SW)]

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

    options = {"ShowLeader": Options(True, pygame.K_5, "ShowLeader", 0, 80),
               "ShowAdd": Options(True, pygame.K_2, "ShowAdd", 0, 20),
               "ShowTotal": Options(True, pygame.K_3, "ShowTotal", 0, 40),
               "ShowRGB": Options(True, pygame.K_6, "ShowRGB", 0, 100),
               "ShowRGBBase": Options(True, pygame.K_7, "ShowRGBBase", 0, 120),
               "ShowSum": Options(True, pygame.K_4, "ShowSum", 0, 60),
               "CycleColors": VisualOptions(False, pygame.K_F6, "CycleColors"),
               "opsOnTop": VisualOptions(True, pygame.K_UP, "opsOnTop"),
               "ShowFps": Options(True, pygame.K_1, "ShowFps", 0, 0),
               "ShowAVGPos": VisualOptions(False, pygame.K_p, "ShowAVGPos"),
               "ShowAVG": Options(True, pygame.K_8, "ShowAVG", 0, 140)}

    FPSCap = 120

    #sounds
    sounds = {"windows": pygame.mixer.Sound(r".\src\Sounds\WINXP_Startup.wav"), 
           "THX": pygame.mixer.Sound(r".\src\Sounds\THX_Sound.wav"), 
           "disney": pygame.mixer.Sound(r".\src\Sounds\Disney.wav"),
           "pixar": pygame.mixer.Sound(r".\src\Sounds\Pixar.wav"),
           "fox": pygame.mixer.Sound(r".\src\Sounds\Fox.wav"),
           "clap": pygame.mixer.Sound(r".\src\Sounds\Clap.wav"),
           "error": pygame.mixer.Sound(r".\src\Sounds\error.wav")}

    avgPosDVD = AvgPosDVD(winWidth, winHeight, DVD_Logos, SH, SW, SX=mean([x.SX for x in DVDSList]), SY=mean([y.SY for y in DVDSList]))
    clock = pygame.time.Clock()

    while (Run := True):
        clock.tick(FPSCap)
        for event in pygame.event.get(): #mouse clicks and button presses
            if event.type == pygame.QUIT: pygame.quit(); Run = False; break
            if event.type == pygame.KEYDOWN: DVDSList, options, sounds, Run = mainKeyChks(DVDSList, options, sounds, Run, win)  
            if event.type == pygame.MOUSEBUTTONDOWN: ADD, DVDSList, R, G, B, baseColor = mouseChks(options, ADD, DVDSList, SH, SW, R, G, B, baseColor, event, DVD_Logos, inverseRGBColor)    
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                winWidth, winHeight = pygame.display.get_surface().get_size()
        else: #key checks
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and keys[pygame.K_LSHIFT]: FPSCap += 1
            if keys[pygame.K_DOWN] and keys[pygame.K_LSHIFT]: FPSCap -= 1
            if keys[pygame.K_ESCAPE] or keys[pygame.K_PAUSE]:
                pygame.quit()
                Menu().mainMenu()
            elif (keys[pygame.K_ESCAPE] and keys[pygame.K_LSHIFT]) or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.quit(); Run = False; break

            if len(DVDSList) > 1 and options["ShowAVGPos"].on and avgPosDVD.Move: 
                avgPosDVD.findAVGPos(DVDSList) #sets avgx, avgy
                        
            inverseRGBColor = (255 - R, 255 - G, 255 - B) #sets inverse color

            if options["CycleColors"].on: R, G, B, baseColor = cycleColors(R, G, B, baseColor)
            
            #setting stats
            if hits := [x.wallHits for x in DVDSList]:
                leaders, totalHits = max(hits), sum(hits)
                AVGHits = mean(hits) if len(hits) >= 2 else totalHits

            #rendering
            for DVD in DVDSList: 
                if DVD.Move: DVD.move()
                if type(DVD) is InverseColorDVD:
                    DVDSList, DVD_Logos = DVD.recolorInverseDVDS(DVDSList, inverseRGBColor, DVD_Logos)
                    
            win.fill((R, G, B))
            #options rendering
            if not options["opsOnTop"].on:
                renderDVDS(fonts, DVDSList, inverseRGBColor, win, options)
            for op in options.values():
                if op.on:
                    if op.name == "ShowLeader": blitOps(fonts, "mainFont", f'MOST HITS (5): {leaders}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowAdd": blitOps(fonts, "mainFont", f'ADD (2): {ADD}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowTotal": blitOps(fonts, "mainFont", f'DVDS (3): {len(DVDSList)}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowRGB": blitOps(fonts, "DVDInfoFont", f'RGB (6): {R, G, B}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowRGBBase": blitOps(fonts, "DVDInfoFont", f'RGB Base(7): {baseColor}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowSum": blitOps(fonts, "mainFont", f'TOTAL HITS (4): {totalHits}', inverseRGBColor, op.xRend, op.yRend)
                    if op.name == "ShowFps": blitOps(fonts, "DVDInfoFont", f'FPS (1): {round(clock.get_fps(), 2)}', inverseRGBColor, op.xRend, op.yRend)
                    
                    if op.name == "ShowAVG": blitOps(fonts, "DVDInfoFont", f'AVG HITS (8): {AVGHits}', inverseRGBColor, op.xRend, op.yRend)
            if options["opsOnTop"].on:
                renderDVDS(fonts, DVDSList, inverseRGBColor, win, options)
            
            pygame.display.update()
            
def mainInit(winwidth, winheight, sh, sw):
    global SH, SW, winWidth, winHeight

    SH, SW = int(sh), int(sw)
    winWidth, winHeight = winwidth, winheight
    pygame.init(); pygame.mixer.init(); pygame.font.init()
    main()