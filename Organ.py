import numpy as np
from Config import *
from Functions import *

# "head" =  0
# "boca" =  1
# "roda" =  2
# "antenaR"= 3
# "antenaG"=4
# "memory"= 5
# "internalstate = 6"
# "EGG"=7
# "null"=   9
class organ():
    def __init__(self, gene, type = None, location = None, ingene=None, outgene = None, bias = None, forca = None, dim = None, EPA= None, action = 0.0, color = None ):
        self.gene = np.copy(gene)
        elprob = 0.1
        np.random.seed(54)
        e_seed = np.random.rand(self.gene.shape[1]) * 2 - 1
        e = np.sin(np.sum(self.gene[0] * e_seed))

        if type == None:
            np.random.seed(50)
            a_seed = np.random.rand(self.gene.shape[1])*2-1
            np.random.seed(51)
            b_seed = np.random.rand(self.gene.shape[1]) * 2 - 1
            np.random.seed(52)
            c_seed = np.random.rand(self.gene.shape[1]) * 2 - 1
            np.random.seed(53)
            d_seed = np.random.rand(self.gene.shape[1]) * 2 - 1


            a = np.sin(np.sum(self.gene[1]*a_seed))
            b = np.sin(np.sum(self.gene[1]*b_seed))
            c = np.sin(np.sum(self.gene[1]*c_seed))
            d = np.sin(np.sum(self.gene[1]*d_seed))



            np.random.seed(None)
           
            if e> 0:


                if a <= 0 and b <= 0 and c <= 0:
                    type = 3

                if a <= 0 and b <= 0 and c > 0:
                    type = 2

                if a <= 0 and b > 0 and c <= 0:
                    type = 5

                if a <= 0 and b > 0 and c > 0:
                    type = 6

                if a > 0 and b <= 0 and c <= 0:
                    type = "EGG"

                if a > 0 and b <= 0 and c > 0:
                    type = 3

                if a > 0 and b > 0 and c <= 0:
                    type = 2

                if a > 0 and b > 0 and c > 0:
                    type = 3
            else:

                type = 9


            np.random.seed(seed=None)
        if ingene == None:
            np.random.seed(2)
            ingene = np.random.random((3,gene.shape[0], gene.shape[1]))*2-1
            np.random.seed(seed = None)

        if outgene == None:
            np.random.seed(3)
            outgene = np.random.random((3,gene.shape[0], gene.shape[1]))*2-1
            np.random.seed(seed=None)
        if bias == None:
            bias = np.random.random((gene.shape[0], gene.shape[1]))

        if location == None:
            np.random.seed(70)
            loc_seedA = np.random.rand(self.gene.shape[1]) * 2 - 1
            np.random.seed(701)
            loc_seedB = np.random.rand(self.gene.shape[1]) * 2 - 1

            location = abs(np.sin(np.sum(self.gene[0]))) * 2*math.pi# * loc_seedA  )/np.sum(self.gene[1] * loc_seedB))) * 2*math.pi

            #location = (self.gene[0,4]+self.gene[0,5]+self.gene[0,6]+self.gene[0,7])*2*math.pi
            #location = np.sum(self.gene[0])*10 * math.pi
            # if type == "EGG":
            #     location = math.pi


        if dim == None:
            np.random.seed(71)
            dim_seedA = np.random.rand(self.gene.shape[1]) * 2 - 1
            np.random.seed(711)
            dim_seedB = np.random.rand(self.gene.shape[1]) * 2 - 1

            dim = abs(np.sin(np.sum(self.gene[1] * dim_seedA)))*15+1


            #dim = np.clip(abs(self.gene[0,5]/self.gene[0,6]),2,50)
            #dim = abs(self.gene[0,8]+self.gene[0,12]+self.gene[0,10]+self.gene[0,11])*12
        if forca == None:
            np.random.seed(72)
            forca_seedA = np.random.rand(self.gene.shape[1]) * 2 - 1
            np.random.seed(724)
            forca_seedB = np.random.rand(self.gene.shape[1]) * 2 - 1
            forcab = np.sin(np.sum(self.gene[1] * forca_seedA))#/np.sum(self.gene[1] * forca_seedB))
            forca = e

            #forca = np.tanh(self.gene[0,7]/self.gene[0,8])*4
            #forca = gene[0,0]-self.gene[0,9]#-self.gene[0,9]
            #forca = np.sum(self.gene[0])
            #forca =(self.gene[0, 0] + elprob-self.gene[0,9])*2
            np.random.seed(seed=None)
        if color == None:
            np.random.seed(22)

            R_random = ((np.random.rand(gene.shape[1])*2)-1)

            np.random.seed(23)
            G_random = ((np.random.rand(gene.shape[1])*2)-1)

            np.random.seed(24)
            B_random = ((np.random.rand(gene.shape[1])*2)-1)
            np.random.seed(seed=None)
            #
            # R = np.abs(np.sin(np.sum(gene[0]*R_random)))
            # G = np.abs(np.sin(np.sum(gene[0]*G_random)))
            # B = np.abs(np.sin(np.sum(gene[0] * B_random)))

            R = np.abs(np.sin(np.sum(gene[0] * R_random)*2))
            G = np.abs(np.sin(np.sum(gene[0] * G_random)*2))
            B = np.abs(np.sin(np.sum(gene[0] * B_random)*2))

            color = np.array([R,G,B])
            color = color/color.max()





        self.type =type
        self.location = location
        self.dim = dim
        self.forca = forca
        self.forcab = forcab
        self.ingene = ingene
        self.outgene = outgene
        self.bias = (bias*2-1)
        self.EPA = EPA
        self.action = action
        self.color = color
        self.trigger = 0
        self.threshold = (np.tanh(np.sum(self.gene[1]))+1)*0.5*1000+300
        self.previous = 0.0

    def calc(self, a, calculate = True):

        if self.type == 9 or self.type == 0:
            pass



        if self.type == 3:
            #a = (a+self.previous)/2
            aa = np.sum(a*self.color)

            result = np.tanh(aa*self.forca * self.gene[1]*0.1)# + np.tanh(self.action)*self.gene[0]*self.forca*0.1
            self.action = aa
            self.previous = a
            return result


        # egg
        if self.type == "EGG":
            eggactivity = np.tanh(np.sum(a * self.gene[1]))
            #   print eggactivity
            if eggactivity > 0.2:

                return True

            else:
                return False







        if self.type == 2:

            #print "ssss" + str(self.forca)
            result = np.tanh(np.sum(a*self.gene[1]))*self.forca*10
            self.action = result
            return result

        if self.type == 1:
            result = np.tanh(np.sum(a * self.gene[1]))
            self.action = result
            #result = self.forca
            return result

        #memoria
        if self.type == 5:
            if calculate is True:
                offset = 0.2

                calculated_val = np.tanh(np.sum(a*self.gene[0]))

                if calculated_val > offset:
                    self.action +=0.5*self.forcab
                else:
                    self.action -=0.1*self.forcab
                self.action = np.clip(self.action, 0, 1)
             

            else:

                result = self.action*self.gene[1]*self.forca
                #print self.action
                #self.action = self.action -(self.action*self.forca)
                # if self.action <= 0:
                #     self.action = 0
                #
                # if self.action >= 100:
                #     self.action = 100
                return result

        if self.type == 6:
            np.random.seed(601)
            a0 = np.random.random(self.gene[1].shape)*2-1
            a0 *= a[0]
            np.random.seed(602)
            a1 = np.random.random(self.gene[1].shape)*2-1
            a1 *= a[1]
            aa = a0 +a1

            result = np.tanh(aa*self.forca* self.gene[1])
            np.random.seed()
            return result










