from bug import bug
from Functions import *

#classe da simulacao
class simulation():
    def __init__(self, bugs = None,
                 environment=None,
                 bugmap = [[None for _ in range(10)] for _ in range(10)],
                 step = 0,
                 #champions = [bug()for i in range(30)],
                 championsR=[bug()for i in range(0)],
                 championsG=[bug()for i in range(0)],
                 championsB=[bug()for i in range(0)],
                 foodammount=400000,

                 radiation=0.003,
                 reproductions = 0):

        if bugs == None:
            self.bugs = []
            self.bugs.append(bug())

            for i in range(80):
                self.bugs.append(bug())

        if environment == None:
            environment = []


            environment.append(distribute(foodammount, prob=10)*1)
            environment.append(distribute(foodammount, prob=10)*1)
            environment.append(distribute(foodammount, prob=10)*1)
            environment.append(distribute(foodammount, prob=10) * 1)


        self.step = step
        self.bugmap = bugmap
        self.environment = environment
        self.championsR = championsR
        self.championsG = championsG
        self.championsB = championsB
        self.foodammount = foodammount
        self.radiation = radiation
        self.reproductions = reproductions
        self.backgroundpower = 20.0
        self.draw = True

        self.lastchampion = bug()
        self.lastchampionR = bug()
        self.lastchampionG = bug()
        self.lastchampionB = bug()
        self.championR_score = 0
        self.championG_score = 0
        self.championB_score = 0
        self.contrast = 1
        self.maxfoodammount=400000
        self.terrainview = False




    def decompose(self, bug):
        if bug != None:

            coordenada_do_bicho = (t(bug.position[0]), t(bug.position[1]))
            comidatotal = (bug.eatenR +bug.eatenG+bug.eatenB)
            quantidade = get_ratio(bug.color)-get_ratio(bug.color).min()
            if np.sum(quantidade) > 0:
                quantidade /=np.sum(quantidade)

            food_color_ratio = 0.5
            anti_food_color_ratio = 1-food_color_ratio
            quantidadeR = comidatotal * quantidade[0]*food_color_ratio + bug.eatenR*anti_food_color_ratio
            quantidadeG = comidatotal * quantidade[1]*food_color_ratio + bug.eatenG*anti_food_color_ratio
            quantidadeB = comidatotal * quantidade[2]*food_color_ratio + bug.eatenB*anti_food_color_ratio

            quantidadeR = comidatotal *0.33*anti_food_color_ratio + comidatotal*quantidade[0]*food_color_ratio*0.33
            quantidadeG = comidatotal *0.33*anti_food_color_ratio + comidatotal*quantidade[1]*food_color_ratio*0.33
            quantidadeB = comidatotal *0.33*anti_food_color_ratio + comidatotal*quantidade[2]*food_color_ratio*0.33
            contrastmult = 1
            radiusmult = 1
            addcrop(self.environment[0], int(bug.exploderadius[0]*(np.clip(float(bug.age)*0.00005*0.5,0,2)+1))*radiusmult, quantidadeR, coordenada_do_bicho, contrast=10*self.contrast)
            addcrop(self.environment[1], int(bug.exploderadius[1]*(np.clip(float(bug.age)*0.00005*0.5,0,2)+1))*radiusmult, quantidadeG, coordenada_do_bicho, contrast=5*self.contrast)
            addcrop(self.environment[2], int(bug.exploderadius[2]*(np.clip(float(bug.age)*0.00005*0.5,0,2)+1))*radiusmult, quantidadeB,coordenada_do_bicho, contrast=2*self.contrast)
            #addcrop(self.environment[3],int(bug.exploderadius[3] * (np.clip(float(bug.age) * 0.00005 * 0.25, 0, 2) + 1)) * 1, quantidadeB,coordenada_do_bicho, contrast=1)

    #calcula cada passo da simulacao
    def epoch(self):
        if self.step ==1:
            self.drawchampions()
        bsimwindow.fill([0,0,0,0])
        backgroundwindow.unlock()
        
        self.Calculate_bugs()
        self.step +=1
        self.bugs = filter(None, self.bugs)
        # apaga os bugs da lista que passaram a ser None
        if len(self.bugs) > maxbugnumber:
            randombugindex = random.randint(0, len(self.bugs) - 1)
            if self.bugs[randombugindex] != None:
                self.bugs[randombugindex].energy = 10
        
        self.bugs.sort(key=lambda x: float(x.energyhistory)+(x.eatenR+x.eatenG+x.eatenB)*0.1, reverse=True)

        if self.step % 500 == 0 and len(self.bugs) > 0:
            self.addchampion()

            self.drawchampions()

        if self.step % 100 == 0:


            ratioR = 0.9
            antiratioR = 1 -ratioR

            ratioG = 0.9
            antiratioG = 1 - ratioG

            ratioB = 0.9
            antiratioB = 1 - ratioB

            envblurR = blur(self.environment[0])
            envblurG = blur(self.environment[1])
            envblurB = blur(self.environment[2])


            self.environment[0] = envblurR*antiratioR + self.environment[0]*ratioR
            self.environment[1] = envblurG*antiratioG + self.environment[1]*ratioG
            self.environment[2] = envblurB*antiratioB+ self.environment[2]*ratioB

            # self.environment[0] = bb[:, :, 0] * antiratioR + self.environment[0] * ratioR
            # self.environment[1] = bb[:, :, 1] * antiratioG + self.environment[1] * ratioG
            # self.environment[2] = bb[:, :, 2] * antiratioB + self.environment[2] * ratioB


            totalfood = np.sum(np.array(self.environment[0]+self.environment[1]+self.environment[2]))
            self.environment = np.clip(self.environment / totalfood * self.foodammount, 0, 50)
            self.environment[3] = self.environment[3] / np.sum(self.environment[3]) * 5000

            # if totalfood < self.foodammount:
            #
            #     self.environment[0] += distribute( (self.foodammount-totalfood)*0.001, prob=0.1)
            #     self.environment[1] += distribute((self.foodammount-totalfood)*0.001, prob=0.1)
            #     self.environment[2] += distribute((self.foodammount-totalfood)*0.001, prob=0.1)
            # else:
            #
            #     self.environment = np.clip(self.environment/ totalfood * self.foodammount,0,255)
            #     self.environment[3] = self.environment[3]/np.sum(self.environment[3])*5000

    def addchampion(self, bug=None):
        if bug == None:
            numberofchampions = 10
            bugR = None
            bugG = None
            bugB = None

            for i in range(10):

                if np.argmax(self.bugs[i].color) == 0 and bugR == None:
                    bugR = self.bugs[i]

                if np.argmax(self.bugs[i].color) == 1 and bugG == None:
                    bugG = self.bugs[i]

                if np.argmax(self.bugs[i].color) == 2 and bugB == None:
                    bugB = self.bugs[i]

            if bugR !=None:
                if bugR not in self.championsR:
                    self.championsR.insert(0, bugR)

            if bugG != None:
                if bugG not in self.championsG:
                    self.championsG.insert(0, bugG)

            if bugB != None:
                if bugB not in self.championsB:
                    self.championsB.insert(0, bugB)



            if len(self.championsR) > numberofchampions:
                del self.championsR[np.random.randint(0,len(self.championsR))]

                self.championsR = filter(None, self.championsR)

            if len(self.championsG) > numberofchampions:
                del self.championsG[np.random.randint(0,len(self.championsG))]
                self.championsG = filter(None, self.championsG)

            if len(self.championsB) > numberofchampions:
                del self.championsB[np.random.randint(0,len(self.championsB))]
                self.championsB = filter(None, self.championsB)
        else:
            if np.argmax(bug.color) == 0:
                self.championsR.insert(0, bug)

            if np.argmax(bug.color) == 1:
                self.championsG.insert(0, bug)

            if np.argmax(bug.color) == 2:
                self.championsB.insert(0, bug)



    def propagate(self, bug):

        if bug.ovary != None:


                for ovary in bug.ovary:

                    if bug.state == "alive" and ovary.calc(bug.brainstate):

                        ovary.action += abs(ovary.forca)*2
                        bug.energy -= abs(ovary.forca)*2



                    if ovary.action > ovary.threshold or (bug.age > 2000 and ovary.action > ovary.threshold/2 ):

                        bug.energyhistory += 1000

                        for u in range(bug.eggammount):
                            bugmate = bug

                            if 0.5 > np.random.random():
                                bestscore = 100000

                                for i in range(10):
                                    possiblemate = self.bugs[i]
                                    if possiblemate != None and possiblemate != bug:

                                        testscore = np.sum(np.abs(np.array(possiblemate.gene[0]) - np.array(bug.gene[0])))
                                        if testscore < bestscore:
                                            bestscore = testscore
                                            bugmate = self.bugs[i]

                                if testscore > 2:
                                    bugmate = bug




                                # if np.argmax(bug.color) == 0:
                                #     collection = self.championsR
                                #
                                # if np.argmax(bug.color) == 1:
                                #     collection = self.championsG
                                #
                                # if np.argmax(bug.color) == 2:
                                #     collection = self.championsB
                                #
                                # championscore = 100000
                                # for champion in collection:
                                #
                                #     testscore = np.sum(np.abs(np.array(champion.gene)-np.array(bug.gene)))
                                #     if testscore<championscore:
                                #         bugmate =  champion
                                #         championscore = testscore

                            else:
                                bugmate = bug



                            self.reproductions += 1

                            positionx = float(bug.position[0]+(np.random.random()*2-1)*10)
                            positiony = float(bug.position[1] + (np.random.random() * 2 - 1) * 10)

                            newegg = bug.reproduce(bugmate, position=[positionx, positiony], mutationrate= self.radiation)
                            newegg.energy = ovary.action/bug.eggammount
                            self.bugs.append(newegg)


                        ovary.action = 0
                        #bug.energy -= 500




        if bug.age == 2000 and bug.energy > 600:
            positionx = float(bug.position[0] + (np.random.random() * 2 - 1) * 10)
            positiony = float(bug.position[1] + (np.random.random() * 2 - 1) * 10)
            self.reproductions += 2



            self.bugs.append(bug.reproduce(bug, position=[positionx, positiony], mutationrate=self.radiation))
            self.bugs.append(bug.reproduce(bug, position=[positionx, positiony], mutationrate=self.radiation))
            bug.energy -= 600

        # if bug.energy>2000:
        #     positionx = float(bug.position[0] + (np.random.random() * 2 - 1) * 10)
        #     positiony = float(bug.position[1] + (np.random.random() * 2 - 1) * 10)
        #     self.reproductions += 2
        #     self.bugs.append(bug.reproduce(bug, position=[positionx, positiony], mutationrate=self.radiation))
        #     self.bugs.append(bug.reproduce(bug, position=[positionx, positiony], mutationrate=self.radiation))
        #
        #     #self.decompose(bug)
        #     self.addchampion(bug)
        #     bug.state = "dead"
        #


        if bug.age > 2000:

            if 0.005> np.random.random():

                if bug.energy > 1050:
                    self.addchampion(bug)
                self.decompose(bug)
                bug.state = "dead"

    def Calculate_bugs(self):

        for b in range(len(self.bugs)):

            if self.bugs[b] != None:

                self.bugs[b].bugwalk(self.environment)
                self.propagate(self.bugs[b])

                if self.bugs[b] != None:
                    if self.bugs[b] .energy <= 0 or self.bugs[b].state == "dead":
                        self.bugs[b].energy = 0

                        self.decompose(self.bugs[b] )
                        self.bugs[b].eaten = np.array([0, 0, 0])
                        self.bugs[b] = None

    def addbug(self):
        self.bugs.append(bug())

    def drawchampions(self):


        champions_layer.fill((0,0,0,0))
        champions_title = myfont.render("Champions", 2, (128, 128, 128))

        pygame.draw.rect(champions_layer,[50,50,50],[10,0,142,340],1)
        champions_layer.blit(champions_title,(40,5))
        champnumber = 0
        for champion in self.championsR:
            if self.championsR.index(champion) < 10:
                champion.drawbug()
                champions_layer.blit(champion.surface, (20, champnumber*30+20))
                champnumber +=1
        champnumber = 0
        for champion in self.championsG:
            if self.championsG.index(champion) < 10:
                champion.drawbug()
                champions_layer.blit(champion.surface, (20+35, champnumber*30+20))
                champnumber +=1
        champnumber = 0
        for champion in self.championsB:
            if self.championsB.index(champion) < 10:
                champion.drawbug()
                champions_layer.blit(champion.surface, (20 + 70, champnumber * 30+20))
                champnumber += 1



    #desenha todos os elementos da simulacao
    def display(self, debug = False, background = True, selectedbug = None):


        label_step = myfont.render("Step: " + str(self.step), 2, (255, 255, 255))
        label_number_of_bugs = myfont.render("number of bugs: "+str(len(self.bugs)), 2, (255, 255, 255))
        foodammount_indication = myfont.render("Current food ammount:  "+ str(self.foodammount), 2, (255, 255, 255))
        title = myfontt.render("Newpool 1.5 - Artificial Life simulation - by Filipe Alves 2017 - manalokos@gmail.com", 2,(255, 255, 255))

        screen.fill([0, 0, 0])
        #buttons_layer.fill([0, 0, 0])
        screen.blit(label_step, (200, 10))
        #screen.blit(label_number_of_bugs, (350, 10))

        #screen.blit(foodammount_indication, (500, 50))
        screen.blit(title, (20, 870))
        bigbackground =  pygame.Surface((100, 100))


        #imprime a informacao do background, ou se background for False, imprime o background de 500 em 500 steps
        if background == True or self.step % 100 == 0:
            if self.terrainview is False:


                tempenviro = 20+(255-np.clip(np.array(np.dstack((self.environment[0],self.environment[1],self.environment[2])))*self.backgroundpower,0,255))*0.8
                tempenviro = tempenviro.astype(int)


            else:
                tempenviro = 20 + (np.clip(np.array(np.dstack((self.environment[3], self.environment[3], self.environment[3]))) * self.backgroundpower*2,0, 255)) * 0.8
                tempenviro = tempenviro.astype(int)


            #print backgroundwindow.get_size()
            pygame.surfarray.blit_array(backgroundwindow,tempenviro)


        bigbackground.blit(backgroundwindow, [0, 0])
        bigbackground = pygame.transform.scale(backgroundwindow, (800, 800))
        simwindow.blit(bigbackground,[0,0])

        #imprime o nome do bug selecionado
        if selectedbug != None:
            screen.fill([0,0,0])

            bactivity = myfontt.render("Brain Activity", 2, (255, 255, 255))
            gene_label = myfontt.render("Genes", 2, (255, 255, 255))
            label = myfont.render("Name: " +str(selectedbug.name), 2, (255, 255, 255))
            labelx = myfont.render(str(selectedbug.name), 2, (0,0,0))
            label2 = myfont.render("Age:" + str(selectedbug.age), 2, (255, 255, 255))
            label3 = myfont.render("Energy:" + str(int(selectedbug.energy)), 2, (255, 255, 255))
            label4 = myfont.render("Happy:" + str(selectedbug.happy), 2, (255, 255, 255))
            label5 = myfont.render("Generation:" + str(int(selectedbug.generation)), 2, (255, 255, 255))
            label6 = myfont.render("Energy History:" + str(int(selectedbug.energyhistory)), 2, (255, 255, 255))


            


            selectedbuggene = selectedbug.gene
            brain_state = np.copy(selectedbug.brainstate)

            for x in range(len(brain_state)):
                color = val2color(brain_state[x])
                pygame.draw.rect(genescreen, (color, color, color), (
                x * genecellsize, genecellsize + 30 * (genecellsize * len(selectedbuggene[0]) + 1), genecellsize,
                genecellsize*8))

            pygame.draw.circle(simwindow, (0, 0, 0), [int(selectedbug.position[0]), int(selectedbug.position[1])], 20,
                               1)
            simwindow.blit(labelx, [selectedbug.position[0], selectedbug.position[1] + 30])

            
            screen.blit(label, (20,20))
            screen.blit(bactivity, (20, 295))
            screen.blit(gene_label, (20, 145))
            screen.blit(label2, (20, 40))
            screen.blit(label3, (20, 60))
            screen.blit(label4, (20, 80))
            screen.blit(label5, (20, 100))
            screen.blit(label6, (20, 120))

        label_championscore = myfont.render(
            "Color score:  " + "R: " + str(self.championR_score) + "   G: " + str(self.championG_score) + "   B: " + str(
                self.championB_score), 2, (255, 255, 255))

        screen.blit(buttons_layer,(0,0))
        screen.blit(genescreen, (20, 160))
        screen.blit(label_step, (200, 10))
        screen.blit(label_number_of_bugs, (360, 10))
        screen.blit(foodammount_indication, (360, 30))
        screen.blit(label_championscore, (700, 30))
            
        screen.blit(bugview, (100,95))
        screen.blit(simwindow, lowercorner)
        screen.blit(bsimwindow, lowercorner)
        screen.blit(title, (20, 870))
        screen.blit(champions_layer,(170,520))

        
        

        pygame.display.update()




        


