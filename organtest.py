from Config import *
from Organ import organ
from bug import bug
from Functions import *

a = bug(np.load("FIPAXYHE.npy"))
b = organ(a.gene[0], type = "null")




for i in range(101):
    
    for j in range(101):
        
        
        #color = val2color(b.calc([math.sin(float(i)/10)*10,math.sin(float(j)/10)*10,0]))
        pygame.draw.rect(genescreen, b.calc([(float(i)*10-5)/5,(float(j)*10-5)/5,]), (j * 2, i*2 , 2, 2))
        #genescreen.blit(label, selectedbug.position)
        screen.blit(genescreen, (20, 100))
        

    pygame.display.update()

