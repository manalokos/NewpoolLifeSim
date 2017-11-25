

import numpy as np
import random
from Config import *
from Functions import *
from Organ import organ
import time


def matrixcalc(elements):
    matrixantenas = []
    matrixrodas = []
    for i in range(len(elements)):
        if elements[i].type == 3 or elements[i].type == 4:

            matrixantenas.append(elements[i].gene[1])
        if elements[i].type == 2:
            matrixrodas.append(elements[i].gene[1])
    a = np.array(matrixantenas)
    b = np.array(matrixrodas)
    matrix = [a,b]
    return matrix

class bug():


    def __init__(self,
                 gene=None,
                 position = None,
                 size = None,
                 elements = None,
                 elementposition = None,
                 brainstate = None,
                 energy = 300.,
                 name = None,
                 collide = 0,
                 color = None,
                 collisionbug = None,
                 die = False,
                 age = 0,
                 generation=0,
                 eatenR = 0,
                 eatenG = 0,
                 eatenB = 0,
                 mem = None,
                 matrix = None,
                 sexy = None,
                 happy = 0,
                 state = "egg",
                 surface = None):


        if gene is None:
            np.random.seed(seed=None)

            #gene = ((np.random.rand(12, 8, 8)*2)-1)/4
            gene = ((np.random.rand(12, 2, 60)*2)-1)*0.5

        if sexy is None:


            # np.random.seed(69)
            # sexyA = np.sin(np.abs(np.sum(np.random.rand(15, 2, 30)*gene))*0.5)
            #
            # np.random.seed(68)
            # sexyB =np.sin(np.abs(np.sum(np.random.rand(15, 2, 30)*gene))*0.5)
            #
            #
            # np.random.seed(67)
            # sexyC = np.sin(np.abs(np.sum(np.random.rand(15, 2, 30)*gene))*0.5)

            np.random.seed(69)
            #print gene.shape
            sexyA = np.abs(np.sum(np.random.random(gene.shape) * gene))

            np.random.seed(68)
            sexyB = np.abs(np.sum(np.random.random(gene.shape) * gene))

            np.random.seed(67)
            sexyC = np.abs(np.sum(np.random.random(gene.shape) * gene))



            np.random.seed(seed=None)
            sexy = np.array([sexyA, sexyB,sexyC])


        np.random.seed(seed = None)
        self.gene = gene

        if elements is None:
            elements = []
            for i in range(len(self.gene)):
                if i == 0:
                    elements.append(organ(self.gene[i], type = 0))


                if i == 1:

                    elements.append(organ(self.gene[i], type=1, location=0))



                if i > 1:
                    neworgan = organ(self.gene[i])
                    #if neworgan.type != 9:
                    elements.append(organ(self.gene[i]))




        self.elements = elements

        if name == None:

            name = generatenamex(self.gene)

        if position == None:

            x = random.randint(0,simsizeX)
            y = random.randint(0, simsizeY)
           # x = random.randint(250, 350)
           # y = random.randint(250, 350)
            position = [x,y]

        if brainstate== None:
            brainstate = np.array(np.copy(self.gene[1,1]))

        if size == None:



            size = int(np.clip(np.sin(abs(np.sum(gene[:,:,-1]))*5)*10,5,10))

        if color == None:

            l1 = np.clip(int((np.sin(np.sum(gene[:,:,-7])*2)+1)*128),0,255)
            l2 = np.clip(int((np.sin(np.sum(gene[:,:,-8])*2)+1)*128),0,255)
            l3 = np.clip(int((np.sin(np.sum(gene[:,:,-9])*2)+1)*128),0,255)

            if l1+l2+l3 ==0:
                l1 = 128
                l2 = 128
                l3 = 128


            color = np.array([l1, l2, l3])


        if mem == None:

            mem = np.empty(self.gene[1].shape[1])*0

        if matrix == None:

            matrix = matrixcalc(self.elements)


        self.position = position
        self.oldposition = position
        self.orientation = random.uniform(-3,3)
        self.size = size
        self.adultsize = size
        self.elements = elements
        self.energy = energy
        self.color = color
        self.energyhistory = 0.0

        floatcolor =  color.astype(float)

        if np.sum(floatcolor) == 0:

            normcolor = 0

        else:

            normcolor = floatcolor / np.sum(floatcolor)


        self.color_ratio = normcolor
        self.name = name
        self.collide = collide
        self.elementposition = elementposition
        self.brainstate= brainstate
        self.collisionbug = collisionbug
        self.die = die
        self.age = age
        self.eatenR = eatenR
        self.eatenG = eatenG
        self.eatenB = eatenB
        self.eatenT = 0.0
        self.generation = generation
        self.mem = mem
        self.matrix = matrix
        self.sexy = sexy
        self.happy = happy
        self.state = state
        self.eggtimer = int(((np.tanh(np.sum(gene[0, :, -7])))+1)*200)
        if surface is None:
            surface = pygame.Surface((50,50),pygame.SRCALPHA, 32)
        self.surface = surface

        rodas = []
        antenas = []
        mem = []
        intstate = []
        ovary =  []

        for element in self.elements:

            if element.type == 2:
                rodas.append(element)
            elif element.type == 3:
                antenas.append(element)
            elif element.type == 5:
                mem.append(element)
            elif element.type == 6:
                intstate.append(element)
            elif element.type == "EGG":
                ovary.append(element)




        self.rodas = rodas

        rodasW = []
        for roda in self.rodas:
            rodasW.append(roda.gene[1])

        self.rodasW = np.array(rodasW)



        self.antenas = antenas


        self.mem = mem
        self.instate = intstate
        self.ovary =  ovary
        #-------------------------------------------------------

        np.random.seed(84)
        mrate = np.random.random(gene.shape[0])
        self.mutationrate = np.clip(np.abs(np.sum(mrate * gene[:, -1, -1])) * 0.1, 0, 1) + .001
        np.random.seed(seed=None)

        np.random.seed(83)
        mrate = np.random.random(gene.shape[0])
        self.explodevalue = int(np.clip(np.abs(np.sum(mrate * gene[:, -1, -1])), 0, 1) * 20 + 1)
        np.random.seed(seed=None)

        np.random.seed(82)

        e1 = int((abs((np.tanh(np.sum(gene[0, :, -3]))) / 2) * 30 + 15))
        e2 = int((abs((np.tanh(np.sum(gene[0, :, -4]))) / 2) * 30 + 15))
        e3 =int(( abs((np.tanh(np.sum(gene[0, :, -5]))) / 2) * 30 + 15))
        e4 = int((abs((np.tanh(np.sum(gene[0, :, -7]))) / 2) * 30 + 15))

        self.exploderadius = [e1,e2,e3, e4]
        self.eggammount = int(((np.tanh(np.sum(gene[0, :, -6])))+1)*1.5)+1
        #print self.eggammount
        np.random.seed(seed=None)





    def sense(self,  environment):

        self.brainstate = np.copy(self.gene[0, 1])
        #bugweights = np.copy(self.gene[0, 1])
        #bbbb = np.copy(self.gene[1, 0])*0.5

        for antena in self.antenas:


            ex = t(antena.EPA[1][0])
            ey = t(antena.EPA[1][1])

            sample = np.array((environment[0][ex][ey],environment[1][ex][ey],environment[2][ex][ey]))

            #print sample

            self.brainstate +=antena.calc(sample)




            #---------------------------------------------------



            #---------------------------------------------------
        for internalstate in self.instate:

            energy = self.energy*0.1
            age = self.age/3000
            a = [energy, age]

            self.brainstate += internalstate.calc(a)

        for memory in self.mem:


            self.brainstate += memory.calc(self.brainstate, calculate = False)


        #self.brainstate += interiorstate
        #self.brainstate = np.tanh(self.brainstate)
        self.brainstate = np.tanh(self.brainstate)
        #---------------------------------------------------



        for memory in self.mem:
            memory.calc(self.brainstate, calculate = True)
        #----------------------------------------------

    def bugeat(self, environment):

        if self.elements[1].EPA != None:

            mouthstate = self.elements[1].calc(self.brainstate)
            if mouthstate > 0:

                currbugpos = [self.elements[1].EPA[0]+np.random.randint(-3,3),self.elements[1].EPA[1]+np.random.randint(-3,3)]


                R = environment[0][t(currbugpos[0]), t(currbugpos[1])]
                G = environment[1][t(currbugpos[0]), t(currbugpos[1])]
                B = environment[2][t(currbugpos[0]), t(currbugpos[1])]
                T = environment[3][t(currbugpos[0]), t(currbugpos[1])]
                currentcolor = np.array([R,G,B])

                dentada = calculadentada(currentcolor)
                energia = get_energy_old(self.color, dentada)*np.sum(dentada)
                #print energia
                self.happy = energia
                self.energy += energia
                self.energyhistory += energia



                if R >=dentada[0]:
                    R -= dentada[0]
                    self.eatenR += dentada[0]

                else:
                    self.eatenR += R
                    R = 0
                environment[0][t(currbugpos[0]), t(currbugpos[1])] = R


                if G >= dentada[1]:
                    G -= dentada[1]
                    self.eatenG += dentada[1]

                else:
                    self.eatenG += G
                    G = 0
                environment[1][t(currbugpos[0]), t(currbugpos[1])] = G


                if B >=dentada[2]:
                    B -= dentada[2]
                    self.eatenB += dentada[2]
                else:
                    self.eatenB += B
                    B = 0
                environment[2][t(currbugpos[0]), t(currbugpos[1])] = B

                # if T >=1:
                #     T -= 1
                #     self.eatenT += 1
                # else:
                #     self.eatenT += T
                #     T = 0
                # environment[3][t(currbugpos[0]), t(currbugpos[1])] = T

            self.defecate(environment)

    def bugwalk(self, environment):
        if len(self.antenas) == 0:
            self.state = "dead"
        if self.state == "alive":

            self.size = int(np.clip(np.clip(float(self.eatenR+self.eatenG+self.eatenB)/100,0,1)*self.adultsize,3,100))


            self.oldposition = self.position

            if self.age == 0:
                self.elementpos()
            self.sense(environment)

            drag = 0.99
            x = self.position[0]
            y = self.position[1]
            xx = 0
            yy = 0
            ori = 0
            if random.random() < 0.3:
                self.energy -= 1

            self.age += 1

            # somatorio das contribuicoes de translacao e rotacao dos propulsores

            wheellist = 0
            currbugpos = self.position

            terrain = environment[3][t(currbugpos[0]), t(currbugpos[1])]


            for roda in self.rodas:

                

                drag_terrain =np.tanh(terrain*0.2)#-np.tanh(eG*0.2)-np.tanh(eB*0.2)

                drag = 0.99 - drag_terrain*0.1

                #print drag_terrain

                # a forca sera ligada a um output da rede neuronal

                force = np.tanh(self.matrix[1][wheellist].dot(self.brainstate)) * roda.forca * 5
                roda.action = force
                el_angle = roda.location * 2 * math.pi
                xx += math.cos(self.orientation - el_angle) * force * drag
                yy += math.sin(self.orientation - el_angle) * force * drag
                ori += 0.1 * force + force * (1 - drag)
                energyspent = (abs(force) / 2) #* (abs(force) / 2))  # *drag_terrain
                #print energyspent

                self.energy -= energyspent *0.05
                #print np.power(energyspent,2) * 0.1
                if self.energy < 0:
                    self.energy = 0
                wheellist += 1

            # output do somatorio das trasnforamcoes

            self.orientation = self.orientation + ori

            while self.orientation < 2 * math.pi and self.orientation > 0:
                self.orientation -= 2 * math.pi
            while self.orientation < -2 * math.pi and self.orientation < 0:
                self.orientation += 2 * math.pi

            self.position = [x + xx, y + yy]
            # calcula o movimento da colisao se houver um bug em colisao

            if self.collisionbug != None:
                self.position = [self.position[0] + (self.collisionbug.position[0] - self.position[0]) * -0.2,
                                 self.position[1] + (self.collisionbug.position[1] - self.position[1]) * -0.2]
                self.collisionbug = None

            if self.position[0] > simsizeX - 1:
                self.position[0] = 0

            if self.position[1] > simsizeY - 1:
                self.position[1] = 0

            if self.position[0] < 0:
                self.position[0] = simsizeX - 1

            if self.position[1] < 0:
                self.position[1] = simsizeY - 1

            self.elementpos()
            self.bugeat(environment)
            #self.drawbug()

        if self.state == "egg":
            self.eggtimer -= 1
            self.drawegg()
            if self.eggtimer <= 0:
                self.state = "alive"





    # conversao de coordenadas locais para globais dos elementos do bicho
    def elementpos(self):

        pygame.draw.circle(bsimwindow, [0,0,0,50], np.array(roundvect(self.position))+2, self.size, 0)
        pygame.draw.circle(bsimwindow, self.color, roundvect(self.position), self.size, 0)



        #print self.orientation
        for i in range(len(self.elements)):
            if self.elements[i].type == 6:
                pygame.draw.circle(bsimwindow, [128, 128, 128], roundvect(self.position), self.size / 2, 1)

            if self.elements[i].type == 9 or self.elements[i].type == 0:
                self.elements[i].EPA = None

            # para circulos index 0
            if self.elements[i].type == 2 or self.elements[i].type == 1 and i > 0:
                el = self.elements[i]
                location = el.location

                force = el.forca
                dimension = el.dim


                position = rotatevector([self.size * math.sin(location), self.size * math.cos(location)],
                                        self.orientation)

                el.EPA = roundvect([position[0] + self.position[0], position[1] + self.position[1]])
                if self.elements[i].type == 2:

                    pygame.draw.circle(bsimwindow, [0, 0, 0, 100], self.elements[i].EPA, 2, 1)
                if self.elements[i].type == 1:
                    boca = self.elements[i]
                    if boca.action > 0:

                        pygame.draw.circle(bsimwindow, [255, 255, 255], boca.EPA, 2, )
                    else:
                        pygame.draw.circle(bsimwindow, [0, 128, 255], boca.EPA, 2, )




            if self.elements[i].type == 3 or self.elements[i].type == "EGG":
                el = self.elements[i]
                location = el.location

                dimension = el.dim

                # converte as 2 posicoes
                position = rotatevector([self.size * math.sin(location), self.size * math.cos(location)],
                                        self.orientation)
                position = roundvect([position[0] + self.position[0], position[1] + self.position[1]])
                position2 = rotatevector(
                    [(self.size + dimension) * math.sin(location), (self.size + dimension) * math.cos(location)],
                    self.orientation)
                position2 = roundvect([position2[0] + self.position[0], position2[1] + self.position[1]])
                el.EPA = [position, position2]


                #draw
                cor = self.elements[i].color * 255
                cor = cor.astype(int)
                if self.elements[i].type == 3:

                    pygame.draw.line(bsimwindow, cor, self.elements[i].EPA[0], self.elements[i].EPA[1], 1)

                if self.elements[i].type == "EGG":
                    ovary = self.elements[i]

                    cor = ovary.color * 255
                    cor = cor.astype(int)

                    ovarysize = int(np.clip(ovary.action / ovary.threshold, 0, 1) * self.size) + 2
                    pygame.draw.circle(bsimwindow, cor, ovary.EPA[0], ovarysize, )
                    pygame.draw.circle(bsimwindow, [0, 0, 0], ovary.EPA[0], ovarysize, 1)


            if self.elements[i].type == 5:
                el = self.elements[i]
                location = el.location

                force = el.forca
                dimension = el.dim

                position = rotatevector(
                    [(self.size/2) * math.sin(location), (self.size/2) * math.cos(location)],
                    self.orientation)

                el.EPA = roundvect([position[0] + self.position[0], position[1] + self.position[1]])

                memoria = self.elements[i]
                memcolor = c(memoria.action  * 256)

                pygame.draw.circle(bsimwindow, [memcolor, 0, memcolor], memoria.EPA, 2, )

    def drawegg(self):
        pygame.draw.circle(bsimwindow, [0, 0, 0, 100], np.array(roundvect(self.position)), self.size-1, 0)
        pygame.draw.circle(bsimwindow, self.color, roundvect(self.position), self.size/2, 0)
        pygame.draw.circle(bsimwindow, [0, 0, 0], roundvect(self.position), self.size/2, 1)

    def drawbug(self):
        offset = 25
        drawpos = np.array((25,25))
        bug = self
        self.surface.fill(color=(0, 0, 0, 0))
        pygame.draw.circle(self.surface, bug.color, (offset, offset), bug.size, 0)



        for antena in bug.antenas:
            el = antena

            locationA = [ -bug.size * math.sin(el.location)+offset,
                         -bug.size * math.cos(el.location)+offset]
            locationB = [-(bug.size + el.dim) * math.sin(el.location) + offset,
                         -(bug.size + el.dim) * math.cos(el.location) + offset]

            cor = el.color * 255
            cor = cor.astype(int)
            pygame.draw.line(self.surface, cor, locationA, locationB, 1)

        for ovary in bug.ovary:
            el = ovary

            locationA = [int( -bug.size * math.sin(el.location)+offset),
                         int(-bug.size * math.cos(el.location)+offset)]
            locationB = [-(bug.size + el.dim) * math.sin(el.location) + offset,
                         -(bug.size + el.dim) * math.cos(el.location) + offset]


            cor = ovary.color * 255
            cor = cor.astype(int)

            ovarysize = int(np.clip(ovary.action / ovary.threshold, 0, 1) * self.size) + 2
            pygame.draw.circle(self.surface, cor, locationA, ovarysize, )
            pygame.draw.circle(self.surface, [0, 0, 0], locationA, ovarysize, 1)


        for i in range(len(bug.elements)):

            if bug.elements[i].type == 4:
                el = bug.elements[i]
                locationA = [-bug.size * math.sin(el.location) + offset,
                              -bug.size * math.cos(el.location) + offset]
                locationB = [
                    -(bug.size + el.dim) * math.sin(bug.elements[i].location) + offset,
                    -(bug.size + el.dim) * math.cos(bug.elements[i].location) + offset]
                pygame.draw.line(self.surface, [200, 0, 0], locationA, locationB, 1)

            if bug.elements[i].type == 2:
                # print np.abs(np.array([0,0.1,1])*bug.elements[i].action)*255
                wheelcolor = np.clip(np.array([-1, 0.1, 1]) * bug.elements[i].action * 255, 0, 255)
                wheelcolor = wheelcolor.astype(int)

                el = bug.elements[i]
                locationA = [int(-bug.size * math.sin(el.location) + offset),
                             int(-bug.size * math.cos(el.location) + offset)]

                pygame.draw.circle(self.surface, wheelcolor, locationA, 2, )
                pygame.draw.circle(self.surface, [200, 200, 200], locationA, 2, 1)

            if bug.elements[i].type == 1:
                el = bug.elements[i]
                locationA = [int(-bug.size * math.sin(el.location) + offset),
                             int( -bug.size * math.cos(el.location) + offset)]
                if bug.elements[i].action > 0:
                    pygame.draw.circle(self.surface, [0, 255, 255], locationA, 2 , )

                else:
                    pygame.draw.circle(self.surface, [128, 20, 20], locationA, 2, )

            if bug.elements[i].type == 5:
                el = bug.elements[i]
                locationA = [int(-bug.size * math.sin(el.location) / 2 + offset),
                             int(-bug.size * math.cos(el.location) / 2 + offset)]
                memcolor = c(el.action* 256)

                pygame.draw.circle(self.surface, [memcolor, 0, memcolor], locationA, 2 , )

            if bug.elements[i].type == 6:
                pygame.draw.circle(self.surface, [128, 128, 128], (offset, offset), bug.size / 2, 1)



    def mutate(self, intensity=0.2, rate=0.02):


        gene = np.copy(self.gene)
        #mask = (np.random.rand(gene.shape[0], gene.shape[1], gene.shape[2]) < rate).astype(int)
        mask = np.random.choice([0, 1], size=(gene.shape[0], gene.shape[1], gene.shape[2]), p=[1-rate, rate])
        #print mask
        randomgene = np.random.uniform(intensity * -1, intensity, size=(gene.shape[0], gene.shape[1], gene.shape[2]))

        mutatedgene = np.clip(gene + randomgene*mask,-1,1)


        return bug(mutatedgene)

    def reproduce(self, mae, mutationrate=0.02, position = None, energy = 500):
        genP =  self.generation
        genM = mae.generation
        if genP > genM:
            gen = genP
        else:
            gen = genM

        mask = (np.random.rand(self.gene.shape[0], self.gene.shape[1], self.gene.shape[2]) < 0.5).astype(int)
        filhogene = self.gene * mask + mae.gene * (1 - mask)
        filho = bug(filhogene, position = position, generation = gen +1, energy = energy).mutate(rate=mutationrate)
        filho.generation = gen+1
        #filho.selfmutate(intensity = .1,rate=mutationrate)

        if position != None:
            
            filho.position = position
        #return bug(pai.gene)
        return filho
    def defecate(self, environment):

        if 1 > random.random():

            coordenada_do_bichoT = (t(self.oldposition[0] ), t(self.oldposition[1] ))
            quantidadeT =1
            environment[3][coordenada_do_bichoT] += quantidadeT
            self.eatenT = np.clip(self.eatenT -quantidadeT,0,1000000)


        if 0.02 > random.random():
            ammount = 0.1
            coordenada_do_bichoR = (t(self.oldposition[0]+ random.randint(-3,3)), t(self.oldposition[1]+random.randint(-3,3)))
            coordenada_do_bichoG = (t(self.oldposition[0] + random.randint(-3, 3)), t(self.oldposition[1] + random.randint(-3, 3)))
            coordenada_do_bichoB = (t(self.oldposition[0] + random.randint(-3, 3)), t(self.oldposition[1] + random.randint(-3, 3)))
            comidatotal = (self.eatenR + self.eatenG + self.eatenB)


            quantidadeR = (comidatotal * self.color_ratio[0]*0.1 + (self.eatenR * 0.9))*ammount
            quantidadeG = (comidatotal * self.color_ratio[1]*0.1 + (self.eatenG * 0.9))*ammount
            quantidadeB = (comidatotal * self.color_ratio[2]*0.1 + (self.eatenB * 0.9)) *ammount

            # quantidadeR = comidatotal *self.color_ratio[0]*ammount
            # quantidadeG = comidatotal *self.color_ratio[1]*ammount
            # quantidadeB = comidatotal *self.color_ratio[2]*ammount

            self.eatenR = np.clip(self.eatenR - self.eatenR*ammount,0,1000000)
            self.eatenG = np.clip(self.eatenG - self.eatenG*ammount,0,1000000)
            self.eatenB = np.clip(self.eatenB - self.eatenB*ammount,0,1000000)

            environment[0][coordenada_do_bichoR] += quantidadeR
            environment[1][coordenada_do_bichoG] += quantidadeG
            environment[2][coordenada_do_bichoB] += quantidadeB

