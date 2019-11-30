import sys
import pygame
from os import listdir
import tkinter as tk
import random
from DVD_Screen import Menu
from Main import mainInit
import globalFuncs
from Dvds import DVDS

def swap(winWidth, winHeight, sh, sw):
    pygame.display.quit()
    mainInit(winWidth, winHeight, sh, sw)  
    
def main(winWidth, winHeight, sh, sw):
    pygame.init(); pygame.font.init(); pygame.mixer.init()
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("DVD")

    path = "./src/ico_files"
    icos = [str(f'{path}/{x}') for x in listdir(path)if "Menu" not in x and "Main" not in x]
    icos = [pygame.image.load(x) for x in icos]
    pygame.display.set_icon(random.choice(icos))

    Run = True
    path = "./DVD_Logos"
    sw, sh = int(sw), int(sh)
    logos = [str(f'{path}/{x}') for x in listdir(path)]
    DVD_Logos = [pygame.image.load(x) for x in logos]

    DVDSDict = {}

    DVDSDict[1] = DVDS(winWidth, winHeight, DVD_Logos, sh, sw)
    clock = pygame.time.Clock()
    while Run:
        clock.tick(120)
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

            if keys[pygame.K_d]: globalFuncs.randDisMov()
            if keys[pygame.K_p]: globalFuncs.randPixMov()       
                
            win.fill((0, 0, 0))
            for DVD in DVDSDict.values():
                DVD(winWidth, winHeight, DVD_Logos)
                win.blit(DVD.currentLogo, (DVD.SX, DVD.SY))
            pygame.display.update()