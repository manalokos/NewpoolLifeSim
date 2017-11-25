import pygame
import pygame
import random
import string
import math
from pygame import gfxdraw
import numpy as np
from bug import bug
from Simulation import simulation
import Config
from Functions import *
from Organ import *
from Tkinter import Tk
from tkFileDialog import askopenfilename


    

def printbug(bug):
    bugview.fill(color=(0,0,0,0))
    pygame.draw.circle(bugview, bug.color, (150, 150), bug.size * 4, 0)

    # desenha as linhas da lista de elementos
    for antena in bug.antenas:
        el = antena

        locationA = [-4 * bug.size * math.sin(el.location) + 150,
                     -4 * bug.size * math.cos(el.location) + 150]
        locationB = [-4 * (bug.size + el.dim) * math.sin(el.location) + 150,
                     -4 * (bug.size + el.dim) * math.cos(el.location) + 150]

        cor = el.color * 255
        cor = cor.astype(int)
        pygame.draw.line(bugview, cor, locationA, locationB, 2)



    for i in range(len(bug.elements)):



        if bug.elements[i].type == 4:
            el = bug.elements[i]
            locationA = [-4 * bug.size * math.sin(el.location) + 150,
                         -4 * bug.size * math.cos(el.location) + 150]
            locationB = [
                -4 * (bug.size + el.dim) * math.sin(bug.elements[i].location) + 150,
                -4 * (bug.size + el.dim) * math.cos(bug.elements[i].location) + 150]
            pygame.draw.line(bugview, [200, 0, 0], locationA, locationB, 2)

        if bug.elements[i].type == 2:
            #print np.abs(np.array([0,0.1,1])*bug.elements[i].action)*255
            wheelcolor = np.clip(np.array([-1,0.1,1])*bug.elements[i].action*255,0,255)
            wheelcolor= wheelcolor.astype(int)

            el = bug.elements[i]
            locationA = [int(-4 * bug.size * math.sin(el.location) + 150),
                         int(-4 * bug.size * math.cos(el.location) + 150)]

            pygame.draw.circle(bugview, wheelcolor, locationA, 4, )
            pygame.draw.circle(bugview, [200, 200, 200], locationA, 4, 1)

        if bug.elements[i].type == 1:
            el = bug.elements[i]
            locationA = [int(-4 * bug.size * math.sin(el.location) + 150),
                         int(-4 * bug.size * math.cos(el.location) + 150)]
            if bug.elements[i].action > 0:
                pygame.draw.circle(bugview, [0, 255, 255], locationA, 3 * 2, )

            else:
                pygame.draw.circle(bugview, [128,20,20], locationA, 3 * 2, )



        if bug.elements[i].type == 5:
            el = bug.elements[i]
            locationA = [int(-4 * bug.size * math.sin(el.location) / 2 + 150),
                         int(-4 * bug.size * math.cos(el.location) / 2 + 150)]
            memcolor = c((el.action) * 256)

            pygame.draw.circle(bugview, [memcolor, 0, memcolor], locationA, 3 * 2, )

        if bug.elements[i].type == 6:
            pygame.draw.circle(bugview, [128,128,128], (150, 150), bug.size * 4/2, 1)
        for ovary in bug.ovary:
            el = ovary

            locationA = [int(-4 * bug.size * math.sin(el.location) + 150),
                         int(-4 * bug.size * math.cos(el.location) + 150)]

            cor = ovary.color * 255
            cor = cor.astype(int)

            ovarysize = int(np.clip(ovary.action / ovary.threshold, 0, 1) * bug.size) + 2
            pygame.draw.circle(bugview, cor, locationA, ovarysize * 2, )
            pygame.draw.circle(bugview, [0, 0, 0], locationA, ovarysize * 2, 1)

#imprime o gene
def printgene(bug):


    selectedbuggene = bug.gene
    brain_state = bug.brainstate
    genescreen.fill([0,0,0,0])

    for x in range(len(brain_state)):
        color = val2color(brain_state[x])
        pygame.draw.rect(genescreen, (color, color, color), (
        x * genecellsize, genecellsize + 30 * (genecellsize * len(selectedbuggene[0]) + 1), genecellsize, genecellsize))

    for x in range(len(bug.elements)):

        organgene = bug.elements[x].gene

        for z in range(len(selectedbuggene[x])):

            for y in range(len(selectedbuggene[x, z])):
                # print a[x, y, z]

                color = val2color(organgene[z, y])
                dull = remap(color, 0, 255, 50, 90)
                half = remap(color, 0, 255, 0, 90)

                if bug.elements[x].type == 0:
                    pygame.draw.rect(genescreen, (color, color, color), (
                    y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                    genecellsize, genecellsize * 2))


                if bug.elements[x].type == 1:
                    pygame.draw.rect(genescreen, (color, 0, color), (
                        y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                        genecellsize, genecellsize * 2))


                if bug.elements[x].type == 2:
                    pygame.draw.rect(genescreen, (0, 0, color), (
                        y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                        genecellsize, genecellsize * 2))

                if bug.elements[x].type == 3:
                    pygame.draw.rect(genescreen, (0, color, 0), (
                    y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                    genecellsize, genecellsize * 2))


                if bug.elements[x].type == 5:
                    memcolor = c((bug.elements[x].action * 2 + 1) * 256)
                    pygame.draw.rect(genescreen, (color, color, dull), (
                    y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                    genecellsize, genecellsize * 2))

                if bug.elements[x].type == 6:
                    pygame.draw.rect(genescreen, (0, color, color), (
                        y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                        genecellsize, genecellsize * 2))

                if bug.elements[x].type == "EGG":
                    memcolor = c((bug.elements[x].action * 2 + 1) * 256)
                    pygame.draw.rect(genescreen, (color, color, 128), (
                    y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                    genecellsize, genecellsize * 2))


                if bug.elements[x].type == 9:
                    pygame.draw.rect(genescreen, (dull, dull, dull), (
                    y * genecellsize, 2 * z * genecellsize + 2 * x * (genecellsize * len(selectedbuggene[0]) + 1),
                    genecellsize, genecellsize * 2))







def main():
    app_running = True
    sporadicspawn = False
    selectedbugbox = None
    framerate = False
    clock = pygame.time.Clock()
    FPS = 30

    display = True
    debug = False
    background = True
    selectedbug = None

    

    stats_bugnumberR = []
    stats_bugnumberG = []
    stats_bugnumberB = []


    stats_foodammount = []
    stats_repr = [0,0]

    #gera uma simulacao
    sim = simulation()
    sim.display()

    #Main Loop
    while app_running == True:

        

        


        if sim.step % 200 == 0:

            Rbugs = 0
            Gbugs = 0
            Bbugs = 0

            for i in range(len(sim.bugs)):
                if np.argmax(sim.bugs[i].color)==0:
                    Rbugs+=1
                elif  np.argmax(sim.bugs[i].color)==1:
                    Gbugs += 1
                elif np.argmax(sim.bugs[i].color) == 2:
                    Bbugs += 1





            stats_bugnumberR.append(Rbugs)
            stats_bugnumberG.append(Gbugs)
            stats_bugnumberB.append(Bbugs)



            stats_foodammount.append(np.sum(sim.environment[0]+sim.environment[1]+sim.environment[2])/10000)
            
            stats_repr.append(sim.reproductions)
            sim.reproductions=0
            


        sim.epoch()



        if framerate is True:
            clock.tick(FPS)

        if sim.step % 100 == 0 and np.random.random() > 0.9:
            sporadicspawn = True



        while len(sim.bugs) < bugnumber or sporadicspawn == True:# and len(sim.bugs)>len(sim.champions):


            championcolor = np.random.randint(0,3)
            collection = None
            if championcolor == 0:
                collection = sim.championsR

            elif championcolor == 1:
                collection = sim.championsG
            elif championcolor == 2:
                collection = sim.championsB
            if len(collection) > 0:

                randombug = collection[random.randint(0, len(collection)-1)]
                randombug2 = collection[random.randint(0, len(collection) - 1)]
            else:
                randombug = bug()
                randombug2 = bug()
            sporadicspawn = False

            if 0.9 > np.random.random():
                newbug = randombug.reproduce(randombug, mutationrate=sim.radiation*2)
            else:
                newbug = bug()
            newbug.state = "alive"
            sim.bugs.append(newbug)


        if len(sim.bugs) > 100 and sim.step%100 == 0:
             sim.foodammount -= 1000
             if sim.foodammount <=1000:
                 sim.foodammount = 1000
            #Config.toxicity += 0.01

        if len(sim.bugs) < bugnumber+1 and sim.step%100 == 0 and sim.foodammount < sim.maxfoodammount:
             sim.foodammount += 1000
            # if Config.toxicity > 0.6:
            #     Config.toxicity -= 0.01


        if selectedbug != None:
            if selectedbug.energy <= 0:
                selectedbug = sim.bugs[0]

        sim.radiation = button_val("Radiation",20,360,50,20, buttons_layer, sim.radiation,1.1)
            
        sim.contrast = button_val("Decompose Contrast",20,+360+50,50,20, buttons_layer, sim.contrast,1.1)

        sim.maxfoodammount = button_val("MaxFood ammount",20,360+100,50,20, buttons_layer, sim.maxfoodammount,1.1)

        Config.toxicity = button_val("Toxicity",20,360+150,50,20, buttons_layer, Config.toxicity,1.02)

        sim.backgroundpower = button_val("",720,860,50,20, buttons_layer, sim.backgroundpower,1.5)


        

        display =  button_toggle("Realtime",20,560,100,50,buttons_layer, display)

        loadbug = False
        loadbug = button_toggle("Load bug", 20, 560+60, 100, 50, buttons_layer, loadbug)
        if loadbug is True:
            window = Tk()
            window.withdraw()
            filename = askopenfilename()
            if filename:

                for i in range(10):
                    sim.bugs.append(bug(np.load(filename)))

            window.destroy()

        savebug = False
        savebug = button_toggle("Save bug", 20, 560 + 120, 100, 50, buttons_layer, savebug)
        if savebug is True:
            if selectedbug != None:
                np.save(str(selectedbug.name), selectedbug.gene)

        gen_randbug = False
        gen_randbug= button_toggle("rand_bugs", 20, 560 + 180, 100, 50, buttons_layer, gen_randbug)
        if gen_randbug is True:
            for i in range(10):
                sim.bugs.append(bug())
        statistics = False
        statistics = button_toggle("Statistics", 20, 560 + 180+60, 100, 50, buttons_layer, statistics)
        if statistics is True:
            plt.plot(stats_repr)
            plt.plot(stats_bugnumberR, color=(1.0, 0.0, 0.0))
            plt.plot(stats_bugnumberG, color=(0.0, 1.0, 0.0))
            plt.plot(stats_bugnumberB, color=(0.0, 0.0, 1.0))
            plt.plot(stats_foodammount)
            plt.show()
            plt.close()






                    
        



        

        #procura eventos de  pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sim = None
                app_running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_t:
                    if display == True:
                        sim.draw = False
                        display = False

                    else:
                        sim.draw = True
                        display = True

                if event.key == pygame.K_b:
                    if background == True:
                        background = False

                    else:
                        background = True
                if event.key == pygame.K_KP_PLUS:

                    sim.backgroundpower *= 1.5
                    buttons_layer.fill((0,0,0,0))

                if event.key == pygame.K_KP_MINUS:
                    sim.backgroundpower *= 0.75
                    buttons_layer.fill((0, 0, 0,0))

                if event.key == pygame.K_f:
                    if framerate == True:
                       framerate = False

                    else:
                        framerate = True


                if event.key == pygame.K_s:
                    if selectedbug != None:
                        np.save(str(selectedbug.name), selectedbug.gene)

                if event.key == pygame.K_l:
                    window = Tk()
                    window.withdraw()
                    filename = askopenfilename()

                    for i in range(10):
                        sim.bugs.append(bug(np.load(filename)))

                    window.destroy()

                if event.key == pygame.K_0:
                    sim.foodammount +=2000
                    sim.environment[0] += distribute(2000, prob=0.1)

                if event.key == pygame.K_r:
                    for i in range(10):
                        sim.bugs.append(bug())


                if event.key == pygame.K_q:
                    sim.contrast /=1.1

                if event.key == pygame.K_v:
                    if sim.terrainview is False:

                        sim.terrainview = True
                    else:
                        sim.terrainview = False

                   # print "Contrast mult: "+str(sim.contrast)



                if event.key == pygame.K_m:
                    window = Tk()
                    window.withdraw()
                    filename = askopenfilename()
                    imagem = np.array(load_image(filename))

                    sim.environment[0] =(255 - imagem[:, :, 0].T) * 0.2
                    sim.environment[1]=(255 - imagem[:, :, 1].T) * 0.2
                    sim.environment[2]=(255 - imagem[:, :, 2].T) * 0.2
                    window.destroy()

                if event.key == pygame.K_n:
                    np.save("Enviro", np.array(sim.environment))

                if event.key == pygame.K_9:
                    lessfood = (sim.foodammount-2000)/sim.foodammount

                    sim.foodammount -=2000
                    sim.foodammount
                    sim.environment[0]*lessfood

                if event.key == pygame.K_p:

                    plt.plot(stats_repr)
                    plt.plot(stats_bugnumberR,color=(1.0, 0.0, 0.0))
                    plt.plot(stats_bugnumberG, color=(0.0, 1.0, 0.0))
                    plt.plot(stats_bugnumberB, color=(0.0, 0.0, 1.0))
                    plt.plot(stats_foodammount)
                    plt.show()
                    plt.close()

            #seleciona bugs com o rato
            if event.type == pygame.MOUSEBUTTONDOWN:

                #print [int((pygame.mouse.get_pos()[0]-lowercorner[0])/(simsizeX/10)),int((pygame.mouse.get_pos()[1]-lowercorner[1])/(simsizeY/10))]
                mousecoordX = float((pygame.mouse.get_pos()[0]-lowercorner[0]))#/(simsizeX/10)
                mousecoordY =float((pygame.mouse.get_pos()[1] - lowercorner[1]))# / (simsizeY / 10)


                #print mousecoordX,mousecoordY
                distancia = 100000
                for i in range(len(sim.bugs)-1):
                    candidatedistance = distance([mousecoordX,mousecoordY], sim.bugs[i].position)
                    if candidatedistance<distancia:
                        distancia = candidatedistance
                        selectedbug = sim.bugs[i]
                if distancia > 80:
                    selectedbug = sim.bugs[0]


                #
                # if mousecoordX < 10 and mousecoordY < 10 and mousecoordX >= 0 and mousecoordY >= 0:
                # selectedbugbox = sim.bugmap[mousecoordX][mousecoordY]
                #
                #
                #
                #


                if selectedbug!= None:



                    #selectedbug = selectedbugbox[0]
                    printgene(selectedbug)




                else:
                    selectedbug = sim.bugs[0]



        if  selectedbug is None:# and display == True:
            if sim != None:
                if sim.step % 100 == 0 and len(sim.bugs)>0:
                    championbug = sim.bugs[0]
                    printbug(championbug)

        else:
            if sim != None:
               # print selectedbug.energy
                printbug(selectedbug)


        if display== True:
            if sim != None:
                sim.display(debug, background, selectedbug)
        else:
            if sim != None:
                if sim.step % 100 == 0:
                    sim.display(debug,background)

        



                        
                    
                                           
main()
