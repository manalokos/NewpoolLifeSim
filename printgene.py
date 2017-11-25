import pygame
import numpy as np
from Functions import *
cellsize = 5
genescreen = pygame.display.set_mode((200, 600))
genescreen.fill([0,0,0])

a = np.load("FIPAXYHE.npy")




for x in range(len(a)):
    

    for y in range(len(a[x])):
        
        for z in range(len(a[x,y])):
            print a[x,y,z]
            
            color = val2color(a[x,y,z])
            pygame.draw.rect(genescreen, (color, color, color), (z * cellsize, y * cellsize+x*51, cellsize, cellsize))
            #genescreen.blit(label, selectedbug.position)

pygame.display.update()
        

    

