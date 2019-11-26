import pygame; pygame.init(); pygame.font.init()
import os
import subprocess
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter.messagebox import showinfo
import random

#MAIN MENU
def controllsMenu():
    with open("controlls.txt", "r") as CF:
        string = CF.read()
        CTRLSRoot = tk.Tk()

        mainL = tk.Label(CTRLSRoot, text=string, font=("Consolas", 13))
        mainL.pack()

        os.environ['SDL_VIDEO_CENTERED'] = "1"

        CTRLSRoot.mainloop()

def done(root):
    global winHeight, winWidth
    winHeight = winHeight.get()
    winWidth = winWidth.get()
    root.destroy()

def setting(root, winHeightE, winWidthE, winHeight, winWidth):

	winHeight.set(winHeightE.get())
	winWidth.set(winWidthE.get())
	root.after(500, setting, root, winHeightE, winWidthE, winHeight, winWidth)

root = tk.Tk()

showinfo("IMPORTANT", "make sure to press done when done and not close out of the window")

os.environ['SDL_VIDEO_CENTERED'] = "1"

winHeight = tk.IntVar()
winHeight.set(1080)

winWidth = tk.IntVar()
winWidth.set(1920)

tk.Label(text="Window height", font=("MS Reference Sans Serif", 23)).pack()

winHeightE = tk.Entry()
winHeightE.insert(0, winHeight.get())
winHeightE.pack()

tk.Label(text="Window width", font=("MS Reference Sans Serif", 23)).pack()

winWidthE = tk.Entry()
winWidthE.insert(0, winWidth.get())
winWidthE.pack()

doneB = tk.Button(root, command=lambda: done(root), text="done", font=("Valken", 20))
doneB.pack()

controllsB = tk.Button(text="OPEN CONTROLS TEXT FILE", font=("MS Reference Sans Serif", 15), command=lambda: controllsMenu())
controllsB.pack()

setting(root, winHeightE, winWidthE, winHeight, winWidth)

root.mainloop()
#/Main Menu




os.environ['SDL_VIDEO_CENTERED'] = "1"

addFont = pygame.font.SysFont("Alien Encounters", 20)
countFont = pygame.font.SysFont("Alien Encounters", 17)

path = "./DVD_Logos"

Run = True

ADD = 1

DVD_Logos = [pygame.image.load(str(path + "/" + x)) for x in listdir(path)]

DVDSDict = {}




if winWidth == 1920 and winHeight == 1080:
    win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN)
else:
    win = pygame.display.set_mode((winWidth, winHeight))

class DVDS:
    def __init__(self, SX=False, SY=False):
        if not SX:
            SX = random.randint(0, round(winWidth - (.1 * winWidth)))
            SY = random.randint(0, round(winHeight - (.1 * winHeight)))
        self.SX = SX
        self.SY = SY
        self.squareH = 43
        self.squareW = 98
        self.SXGain = random.choice([(winWidth + winHeight) / 2 / 1000, -((winWidth + winHeight) / 2 / 1000)]); self.SYGain = random.choice([self.SXGain, -self.SXGain])
        self.currentLogo = random.choice(DVD_Logos)

    def __call__(self):
        self.SX += self.SXGain
        self.SY += self.SYGain
        if self.SX <= 0 or self.SX + self.squareW >= winWidth:
            tilt = random.uniform(-.1, .1)
            if self.SXGain * (-1 + tilt) == 0:
                self.SXGain *= -1
            else:
                self.SXGain *= (-1 + random.uniform(-.1, .1))
                self.currentLogo = random.choice(DVD_Logos)

        if self.SY <= 0 or self.SY + self.squareH >= winHeight:
            tilt = random.uniform(-.1, .1)
            if self.SYGain * (-1 + tilt) == 0:
                self.SYGain *= -1
            else:
                self.SYGain *= (-1 + random.uniform(-.1, .1))
                self.currentLogo = random.choice(DVD_Logos)
        if self.SXGain == 0:
            self.SX = winWidth / 2
            self.SY = winHeight / 2
            self.SXGain = 1
        if self.SYGain == 0:
            self.SX = winWidth / 2
            self.SY = winWidth / 2
            self.SYGain = 1
        if self.SX + self.squareW > winWidth + 10 or self.SX < -10 or self.SY + self.squareH > winHeight + 10 or self.SY < -10:
            self.SX = 100
            self.SY = 100

DVDSDict[1] = DVDS()

while Run:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            ADD = round(ADD)
            if event.button == 1:
                for a in range(ADD):
                    DVDSDict[len(DVDSDict) + 1] = DVDS()

            elif event.button == 3:
                for a in range(ADD):
                    pos = pygame.mouse.get_pos()
                    DVDSDict[len(DVDSDict) + 1] = DVDS(SX=pos[0], SY=pos[1])

            elif event.button == 2:
                for a in range(ADD):
                    try:
                        del DVDSDict[len(DVDSDict)]
                    except:
                        break
    if Run:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ADD += .1
        if keys[pygame.K_DOWN] and ADD >= .1:
            ADD -= .1
        if keys[pygame.K_PAGEDOWN] and ADD >= 1:
            ADD -= 1
        if keys[pygame.K_PAGEUP]:
            ADD += 1
        if keys[pygame.K_END] and ADD >= 5:
            ADD -= 5
        if keys[pygame.K_HOME]:
            ADD += 5

        if keys[pygame.K_ESCAPE] or keys[pygame.K_PAUSE]:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break

        for DVD in DVDSDict:
            DVDSDict[DVD]()

        win.fill((0, 0, 0))
        add = addFont.render(f'ADD: {ADD}', False, (0, 255, 255))
        countTotal = countFont.render(f'TOTAL: {len(DVDSDict)}', False, (0, 255, 255))
        win.blit(add, (0, 0))
        win.blit(countTotal, (0, 40))

        for DVD in DVDSDict:
            win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].SX, DVDSDict[DVD].SY))
        pygame.display.flip()
        

    else:
        break