import sys
import pygame
from os import listdir
import tkinter as tk
import random
from DVD_Screen import Menu
from Main import mainInit
import globalFuncs

def swap(winWidth, winHeight, sh, sw):
    mainInit(winWidth, winHeight, sh, sw)        
def main(winWidth, winHeight, sh, sw):
    pygame.quit()
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


    class DVDS:
        def __init__(self, SX=False, SY=False, SH=sh, SW=sw):
            if not SX:
                SX = random.randint(0, round(winWidth - sw))
                SY = random.randint(0, round(winHeight - sh))
            self.SX = SX
            self.SY = SY
            self.SH = SH
            self.SW = SW
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
                if event.button == 1: DVDSDict[len(DVDSDict) + 1] = DVDS()           
                elif event.button == 2: del DVDSDict[len(DVDSDict)]
                elif event.button == 3:
                    MPos = pygame.mouse.get_pos()
                    DVDSDict[len(DVDSDict) + 1] = DVDS(SX=MPos[0], SY=MPos[1])
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
            for DVD in DVDSDict: DVDSDict[DVD]()
            for DVD in DVDSDict: win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
            pygame.display.update()