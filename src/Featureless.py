import sys
import pygame
import tkinter as tk
import random
from os import listdir

import globalFuncs
from DVD_Screen import Menu
from Main import mainInit
from Dvds import DVDS

def swap(winWidth, winHeight, sh, sw):
    pygame.display.quit()
    mainInit(winWidth, winHeight, sh, sw)  
    
def main(winWidth, winHeight, sh, sw):
    pygame.init(); pygame.font.init(); pygame.mixer.init()

    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("DVD")

    icos = pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in listdir("./src/ico_files")if "Menu" not in x and "FLess" not in x]))
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in listdir("./DVD_Logos")]

    DVDSDict = {}

    Run = True

    sw, sh = int(sw), int(sh)

    DVDSDict[1] = DVDS(winWidth, winHeight, DVD_Logos, sh, sw)

    clock = pygame.time.Clock()

    FPSCap = 120

    while Run:
        clock.tick(FPSCap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                Run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: DVDSDict[len(DVDSDict) + 1] = DVDS(winWidth, winHeight, DVD_Logos, sh, sw)           
                elif event.button == 2: del DVDSDict[len(DVDSDict)]
                elif event.button == 3:
                    MPos = pygame.mouse.get_pos()
                    DVDSDict[len(DVDSDict) + 1] = DVDS(winWidth, winHeight, DVD_Logos, sh, sw, SX=MPos[0], SY=MPos[1])
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.display.quit(); pygame.quit(); Run = False; break
            if keys[pygame.K_PAUSE]:
                if keys[pygame.K_LSHIFT]: swap(winWidth, winHeight, sh, sw)
                else:
                    pygame.quit()
                    Menu().mainMenu()
            if keys[pygame.K_F12]: swap(winWidth, winHeight, sh, sw)

            if keys[pygame.K_d] and keys[pygame.K_LSHIFT]: globalFuncs.randDisMov()
            if keys[pygame.K_p] and keys[pygame.K_LSHIFT]: globalFuncs.randPixMov()    
            
            if keys[pygame.K_LSHIFT] and keys[pygame.K_UP]: FPSCap += 1 if not keys[pygame.K_LCTRL] else 10
            if keys[pygame.K_LSHIFT] and keys[pygame.K_DOWN]: FPSCap -= 1 if not keys[pygame.K_LCTRL] else 10
                
            win.fill((0, 0, 0))
            for DVD in DVDSDict.values():
                DVD(winWidth, winHeight, DVD_Logos)
                win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
            pygame.display.update()