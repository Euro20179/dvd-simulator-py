import pygame; pygame.init(); pygame.font.init()
import random; import os
from DVD_Screen import Menu
from src.Main import main as m
from src.classes import DVDS

def main(winWidth, winHeight, sh, sw):   
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN) if winWidth == 1920 and winHeight == 1080 else pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("DVD"); pygame.display.set_icon(random.choice([pygame.image.load(f'{"./src/ico_files"}/{x}') for x in os.listdir("./src/ico_files") if "Menu" not in x and "Main" not in x]))
    DVD_Logos = [pygame.image.load(f'{"./DVD_Logos"}/{x}') for x in os.listdir("./DVD_Logos")]
    DVDSList = [DVDS(winWidth, winHeight, DVD_Logos, sh, sw)]
    clock = pygame.time.Clock(); FPSCap = 120
    while True:
        clock.tick(FPSCap)
        for event in pygame.event.get():
            MPos = pygame.mouse.get_pos()
            if (cases := {pygame.QUIT: lambda: exec("pygame.display.quit(); pygame.quit(); return"), pygame.MOUSEBUTTONDOWN: lambda: {1: lambda: DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, sh, sw)), 2: lambda: DVDSList.pop(-1), 3: lambda: DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, sh, sw, SX=MPos[0], SY=MPos[1]))}.get(event.button)() if {1: lambda: DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, sh, sw)), 2: lambda: DVDSList.pop(-1), 3: lambda: DVDSList.append(DVDS(winWidth, winHeight, DVD_Logos, sh, sw, SX=MPos[0], SY=MPos[1]))}.get(event.button) else None}).get(event.type): cases[event.type]()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and keys[pygame.K_LSHIFT]) or (keys[pygame.K_LALT] and keys[pygame.K_F4]): pygame.display.quit(); pygame.quit(); return
        elif keys[pygame.K_ESCAPE] or keys[pygame.K_PAUSE]: pygame.quit(); Menu().mainMenu()
        if keys[pygame.K_F12]: pygame.display.quit(); m(winWidth, winHeight, sh, sw)       
        if keys[pygame.K_LSHIFT]: FPSCap = FPSCap.__add__(1 if not keys[pygame.K_LCTRL] else 10) if keys[pygame.K_UP] else FPSCap.__sub__(1 if not keys[pygame.K_LCTRL] else 10) if keys[pygame.K_DOWN] else FPSCap           
        for DVD in DVDSList: DVD.move()
        win.fill((0, 0, 0))
        win.blits([(DVD.currentLogo, (DVD.SX, DVD.SY)) for DVD in DVDSList])
        pygame.display.update()