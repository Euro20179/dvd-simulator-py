import pygame; pygame.init(); pygame.font.init()
import os as os
from os import listdir
from os.path import isfile, join
import tkinter as tk
import random

def done(root):
    global winHeight
    global winWidth
    winHeight = winHeight.get()
    winWidth = winWidth.get()
    root.destroy()

def setting(root, winHeightE, winWidthE, winHeight, winWidth):

	winHeight.set(winHeightE.get())
	winWidth.set(winWidthE.get())
	root.after(500, setting, root, winHeightE, winWidthE, winHeight, winWidth)

root = tk.Tk()

controllsL = tk.Label(text="Left Click: add logo randomly\nRight Click: add logo at curser\nMiddle Click: remove random logo\n\n", font=(None, 30))
controllsL.pack()

root.geometry("700x700")

winHeight = tk.IntVar()
winHeight.set(1080)


winWidth = tk.IntVar()
winWidth.set(1920)

tk.Label(text="Window height", font=(None, 23)).pack()

winHeightE = tk.Entry()
winHeightE.insert(0, winHeight.get())
winHeightE.pack()

tk.Label(text="Window width", font=(None, 23)).pack()

winWidthE = tk.Entry()
winWidthE.insert(0, winWidth.get())
winWidthE.pack()

doneB = tk.Button(root, command=lambda: done(root), text="done")
doneB.pack()

setting(root, winHeightE, winWidthE, winHeight, winWidth)

root.mainloop()

os.environ['SDL_VIDEO_CENTERED'] = "1"

path = "./DVD_Logos"

Run = True

ADD = 1

DVD_Logos = [pygame.image.load(str(path + "/" + x)) for x in listdir(path)]

DVDSDict = {}

addFont = pygame.font.SysFont("arial", 20)

class DVDS:
    def __init__(self, squareX=False, squareY=False):
        if not squareX:
            squareX = random.randint(0, round(winWidth - (.1 * winWidth)))
            squareY = random.randint(0, round(winHeight - (.1 * winHeight)))
        self.squareX = squareX
        self.squareY = squareY
        self.squareH = 43
        self.squareW = 98
        self.squareXGain = random.choice([(winWidth + winHeight) / 2 / 1000, -((winWidth + winHeight) / 2 / 1000)]); self.squareYGain = random.choice([self.squareXGain, -self.squareXGain])
        self.currentLogo = random.choice(DVD_Logos)

    def __call__(self):
        self.squareX += self.squareXGain
        self.squareY += self.squareYGain
        if self.squareX <= 0 or self.squareX + self.squareW >= winWidth:
            tilt = random.uniform(-.1, .1)
            if self.squareXGain * (-1 + tilt) == 0:
                self.squareXGain *= -1
            else:
                self.squareXGain *= (-1 + random.uniform(-.1, .1))
                self.currentLogo = random.choice(DVD_Logos)

        if self.squareY <= 0 or self.squareY + self.squareH >= winHeight:
            tilt = random.uniform(-.1, .1)
            if self.squareYGain * (-1 + tilt) == 0:
                self.squareYGain *= -1
            else:
                self.squareYGain *= (-1 + random.uniform(-.1, .1))
                self.currentLogo = random.choice(DVD_Logos)

DVDSDict[1] = DVDS()
win = pygame.display.set_mode((winWidth, winHeight))

while Run:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                DVDSDict[len(DVDSDict) + 1] = DVDS()

            elif event.button == 3:
                pos = pygame.mouse.get_pos()
                DVDSDict[len(DVDSDict) + 1] = DVDS(squareX=pos[0], squareY=pos[1])

            elif event.button == 2:
                delete = random.choice(list(DVDSDict.keys()))
                del DVDSDict[delete]
    if Run:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            ADD += .1
        if keys[pygame.K_DOWN]:
            ADD -= .1
        if keys[pygame.K_PAGEDOWN]:
            ADD -= 1
        if keys[pygame.K_PAGEUP]:
            ADD += 1
        if keys[pygame.K_END]:
            ADD -= 5
        if keys[pygame.K_HOME]:
            ADD += 5

        for DVD in DVDSDict:
            DVDSDict[DVD]()

        win.fill((0, 0, 0))
        add = addFont.render(f'ADD: {ADD}', False, (0, 255, 255))
        win.blit(add, (0, 0))

        for DVD in DVDSDict:
            win.blit(DVDSDict[DVD].currentLogo, (DVDSDict[DVD].squareX, DVDSDict[DVD].squareY))
        pygame.display.flip()
        

    else:
        break

