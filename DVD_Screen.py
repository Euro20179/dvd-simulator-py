import pygame
import os as os
from os import listdir
from os.path import isfile, join

import random

winHeight = 1080
winWidth = round(winHeight * 16/9)

os.environ['SDL_VIDEO_CENTERED'] = "1"

path = "./DVD_Logos"

Run = True

squareX = 21
squareY = 10
squareH = 43
squareW = 98
squareXGain = 1.2
squareYGain = 1.2
squareColor = (0, 255, 255)

DVD_Logos = [pygame.image.load(str(path + "/" + x)) for x in listdir(path)]

currentLogo = random.choice(DVD_Logos)

win = pygame.display.set_mode((winWidth, winHeight))

while Run:
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            Run = False
            break
    if Run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
                squareXGain += .01
                squareYGain += .01
        elif keys[pygame.K_DOWN]:
                squareXGain -= .01
                squareYGain -= .01
        squareX += squareXGain
        squareY += squareYGain

        if squareX <= 0 or squareX + squareW >= winWidth:
            squareXGain *= (-1 + random.uniform(-.1, .1))
            squareColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            currentLogo = random.choice(DVD_Logos)

        if squareY <= 0 or squareY + squareH >= winHeight:
            squareYGain *= (-1 + random.uniform(-.1, .1))
            squareColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            currentLogo = random.choice(DVD_Logos)

        win.fill((0, 0, 0))
        win.blit(currentLogo, (squareX, squareY))
        pygame.display.flip()
        

    else:
        break

