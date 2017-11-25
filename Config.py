import pygame
import random
import string
import math
from pygame import gfxdraw
import numpy as np
#import Image
from multiprocessing import Pool

windowX = 1200
windowY = 900

simsizeX = 800
simsizeY = 800
cellsize = 4
genecellsize = 2

bugnumber = 40
maxbugnumber = 120

toxicity = 0.70


lowercorner = [windowX-simsizeX-50,windowY-simsizeY-50]
lowercorner = [360,50]
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15)
myfontt = pygame.font.SysFont("monospace", 10)

screen = pygame.display.set_mode((windowX, windowY))
screen.fill([0,0,0])
pygame.display.set_caption('NewpoolRGB 1.6.9')
simwindow = pygame.Surface((simsizeX, simsizeY))
bsimwindow = pygame.Surface((simsizeX, simsizeY),pygame.SRCALPHA, 32)
backgroundwindow = pygame.Surface((simsizeX/cellsize,simsizeY/cellsize))
backgroundtoblur = pygame.Surface((simsizeX/cellsize,simsizeY/cellsize))
backgroundtoblur_S = pygame.Surface((simsizeX/cellsize*0.5,simsizeY/cellsize*0.5))
buttons_layer = pygame.Surface((windowX, windowY),pygame.SRCALPHA, 32)
champions_layer =  pygame.Surface((600, 600),pygame.SRCALPHA, 32)


infowindow = pygame.Surface((300,500))
genescreen = pygame.Surface((300, 600), pygame.SRCALPHA, 32)
bugview = pygame.Surface((300, 300), pygame.SRCALPHA, 32)





