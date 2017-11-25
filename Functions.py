import random
import random
import string
import math
import matplotlib.pyplot as plt
from Config import *
import Config
from pygame import gfxdraw
import numpy as np
#import Image
from multiprocessing import Pool
from PIL import Image


def blur(a):
    kernel = np.array([[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]])
    kernel = kernel / np.sum(kernel)
    arraylist = []
    for y in range(3):
        temparray = np.copy(a)
        temparray = np.roll(temparray, y - 1, axis=0)
        for x in range(3):
            temparray_X = np.copy(temparray)
            temparray_X = np.roll(temparray_X, x - 1, axis=1)*kernel[y,x]
            arraylist.append(temparray_X)

    arraylist = np.array(arraylist)
    arraylist_sum = np.sum(arraylist, axis=0)
    return arraylist_sum


def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

def envblur(a, ammount):
    aaa = sp.ndimage.filters.gaussian_filter(a, 1, mode='constant')
    return a*antiammount + aaa*ammount

def button_val(msg,x,y,w,h,surface, value, ratio):
    
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(surface, [128,50,50],(x,y,w/2,h))
    pygame.draw.rect(surface, [50,128,50],(x+w/2,y,w/2,h))

    if x+w/2 > mouse[0] > x and y+h > mouse[1] > y:
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                surface.fill((0,0,0,0))
                value /= ratio

    if x+w > mouse[0] > x+w/2 and y+h > mouse[1] > y:
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                surface.fill((0,0,0,0))
                value *= ratio


    msg_text = myfont.render( msg, 2, (128,128,128))
    plus_text = myfont.render( " + ", 2, (0,0,0))
    minus_text = myfont.render( " - ", 2, (0,0,0))
    value_text =  myfont.render( str(value), 2, (255,255,255))

    surface.blit(msg_text, (x,y-20))
    surface.blit(minus_text, (x,y))
    surface.blit(plus_text, (x+w/2,y))  
    surface.blit(value_text, (x+w+5,y))
    return value


def button_toggle(msg,x,y,w,h,surface, value):
    if value is True:
        pygame.draw.rect(surface, [50,128,50],(x,y,w,h))
    else:
        pygame.draw.rect(surface, [128,50,50],(x,y,w,h))
    
    mouse = pygame.mouse.get_pos()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if value is True:

                    
                    value = False
                else:
                    value = True


    if value > 100:
        value = round(value)

    msg_text = myfont.render( msg, 2, (200,200,200))
    
    value_text =  myfont.render( str(value), 2, (255,255,255))

    surface.blit(msg_text, (x+3,y+h/3))


    return value
      


        

    #smallText = pygame.font.Font("freesansbold.ttf",20)
    #t#extSurf, textRect = text_objects(msg, smallText)
    #textRect.center = ( (x+(w/2)), (y+(h/2)) )
    #genescreen.blit(textRect)




def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="float" )
    return data

#roda um vector segundo um angulo theta
def rotatevector(a,theta):

    aa = a[0]*math.cos(theta)-a[1]*math.sin(theta)
    bb = a[0]*math.sin(theta)+a[1]*math.cos(theta)

    return [int(aa),int(bb)]

#arredonda um vector para numeros inteiros
def roundvect(a):
    b = [int(a[0]),int(a[1])]
    return b

#gera nomes automaticos unicos aleatorios
def generatename():

    vogais = "AEIOUY"
    consoantes = "BCDFGHJKLMNPQRSTVWXZ"
    name = random.choice(consoantes)+random.choice(vogais)
    for i in range(3):
        name += random.choice(consoantes)
        name += random.choice(vogais)
    return name

# funcao que passa de coordenadas de simulacao para coordenadas de array bugmap 10x10
def roundvect(a):
    b = [int(a[0]),int(a[1])]
    return b

# calcula a distancia entre 2 vectores
def distance(a,b):
    a = [float(a[0]),float(a[1])]
    b = [float(b[0]),float(b[1])]
    vector = [a[0]-b[0],a[1]-b[1]]
    dist = math.sqrt(vector[0]**2+vector[1]**2)
    return dist

#converte valores de -1 a 1, para cores de pixel de 0 a 255
def val2color(a):
    if a > 1:
        a = 1
    if a < -1:
        a = -1
    a =int((a+1)*127)
    return a

# converte coodenadas de simulacao para indexes de grelha 10x10
def b(a):
    a = int(float(a) / (simsizeX/10))
    if a <= 0:
        a = 0
    if a >= (simsizeX / (simsizeX/10)):
        a = int(simsizeX / (simsizeX/10)) - 1
    return a

# funcao util passa de coordenadas de ecra para indexes do array de environment
def t(a):
    # a = int(float(a) / cellsize)
    # if a <= 0:
    #     a = 0
    # if a >= simsizeX / cellsize:
    #     a = int(simsizeX / cellsize) - 1
    # return a


    a = int(float(a) / cellsize)
    if a <= 0:
        a = (simsizeX / cellsize) -a
    if a >= simsizeX / cellsize:
        a = a -(simsizeX / cellsize)
    return a

# funcao util passa de coordenadas de ecra para indexes do array de environment 2D
def tt(a):
    ax = int(float(a[0]) / cellsize)
    if ax <= 0:
        ax = 0
    if ax >= simsizeX / cellsize:
        ax = int(simsizeX / cellsize) - 1
    ay = int(float(a[1]) / cellsize)
    if ay <= 0:
        ay = 0
    if ay >= simsizeY / cellsize:
        ay = int(simsizeY / cellsize) - 1
    return [ax][ay]

# funcao para manter os valores do array dentro de valores validos de pixel
def c(a):
    if a < 0:
        a = 0
    if a >= 255:
        a = 255

    return a

def remap( x, oMin, oMax, nMin, nMax ):

    #range check
    if oMin == oMax:
        #print "Warning: Zero input range"
        return None

    if nMin == nMax:
        #print "Warning: Zero output range"
        return None

    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result

def mutategene(gene, intensity=0.01, rate=0.05):

    mask = (np.random.rand(gene.shape[0], gene.shape[1], gene.shape[2]) < rate).astype(int)
    intensity = np.random.uniform(intensity * -1, intensity, size=(gene.shape[0], gene.shape[1], gene.shape[2]))

    mutatedgene = gene + intensity * mask

    return mutatedgene

def distribute(value, trail=1, prob=0.0005, inverse = False):
    a = np.random.rand(simsizeX / cellsize, simsizeY / cellsize)
    if inverse is False:

        mask = (np.random.rand(simsizeX / cellsize, simsizeY / cellsize) < prob).astype(float)/(trail+1)
    else:
        mask = (np.random.rand(simsizeX / cellsize, simsizeY / cellsize) < prob).astype(float) * np.clip(trail-100, 0,5000)
        #mask = (np.random.rand(simsizeX / cellsize, simsizeY / cellsize) < prob).astype(int) * np.sqrt(trail)

    while np.sum(mask) == 0:
        mask = (np.random.rand(simsizeX / cellsize, simsizeY / cellsize) < prob).astype(float)


    b = (a * mask)
    b = b/np.sum(b)

    d = value*b



    return d

def w_image(array, name, number):
    #print "banana"

    # Rescale to 0-255 and convert to uint8
    rescaled =(np.clip(array,0,255)).astype(np.uint8)

    im = Image.fromarray(rescaled)
    im.save("teste/"+name+str(number)+".png")

def generatenamex(g):

    gene = g.ravel()


    np.random.seed(1)
    vogais = "AEIOUY"
    consoantes = "BCDFGHJKLMNPQRSTVWXZ"

    a = np.random.random((6,len(gene)))*2-1
    #print int(((np.tanh(np.sum(a[0]*gene))+1)/2)*len(vogais))

    l1 = consoantes[int(((np.tanh(np.sum(a[0]*gene*0.1))+1)/2)*(len(consoantes)-1))]
    l2 = vogais[int(((np.tanh(np.sum(a[1]*gene*0.1))+1)/2)*(len(vogais)-1))]
    l3 = consoantes[int(((np.tanh(np.sum(a[2]*gene*0.1))+1)/2)*(len(consoantes)-1))]
    l4 = vogais[int(((np.tanh(np.sum(a[3]*gene*0.1))+1)/2)*(len(vogais)-1))]
    l5 = consoantes[int(((np.tanh(np.sum(a[4]*gene*0.1))+1)/2)*(len(consoantes)-1))]
    l6 = vogais[int(((np.tanh(np.sum(a[5]*gene*0.1))+1)/2)*(len(vogais)-1))]

    name = l1+l2+l3+l4+l5+l6


    np.random.seed(seed = None)

    return name

def generatecolor(g):
    gene = g.ravel()

    np.random.seed(2)

    a = np.random.random((3, len(gene))) * 2 - 1

    l1 = int(((np.tanh(np.sum(a[0] * gene)) + 1) / 2) * 250)
    l2 = int(((np.tanh(np.sum(a[1] * gene)) + 1) / 2) * 250)
    l3 = int(((np.tanh(np.sum(a[2] * gene)) + 1) / 2) * 250)

    color = [l1, l2, l3]

    np.random.seed(seed=None)

    return color


position = (4, 3)

#calcula coordenadas corrigidas para arrays toricos
def toric(array, coord):
    x = coord[1]
    y = coord[0]
    array_w = array.shape[1]
    array_h = array.shape[0]

    if x >= array_w:
        x = x - array_w

    if x < 0:
        x = array_w + x

    if y >= array_h:
        y = y - array_h

    if y < 0:
        y = array_h + y

    return (x, y)

#adiciona valores em coordenadas de array num mundo torico - para os bichos dispersarem o que comeram durante a vida quando morrem
def addcrop(arrayA, spread, targetvalue, position, contrast=3):

    arrayB = np.power(np.random.uniform(size=(spread, spread)), contrast)
    center = len(arrayB) / 2
    for y in range(len(arrayB)):
        for x in range(len(arrayB[0])):

            ammountY = abs(float(center) - y) / float(center)
            ammountX = abs(float(center) - x) / float(center)
            arrayB[y, x] *= np.power(1 - ammountX,2) * np.power(1 - ammountY,1)

            if y == center  and x == center:
                arrayB[y, x] = 0.0

    arrayB_val = np.sum(arrayB)
    arrayB = arrayB / arrayB_val * targetvalue

    center = len(arrayB) / 2

    for y in range(len(arrayB)):
        for x in range(len(arrayB[0])):
            ammountY = abs(float(center) - y) / float(center)
            ammountX = abs(float(center) - x) / float(center)
            newposition = toric(arrayA, (y + position[1] - center, x + position[0] - center))
            arrayA[newposition] += arrayB[y, x]
    return arrayA

def get_energy_old(color_ratio, bytesize):
    bytesize =get_ratio(bytesize)


    a = np.array(color_ratio).astype("float")
    b = np.array(bytesize).astype("float")
    a = vect_norm(a)
    b = vect_norm(b)
    b = 1-b




    ratio = np.sum(np.abs(a-b))-1.3
    ratio = 1 - np.sum(np.abs(a - b))*Config.toxicity
    #print ratio
    return ratio

def get_energy(a,b, difficulty = 0.7):

    # dentada = np.sum(b)
    # a = np.array(a).astype("float")
    # b = np.array(b).astype("float")
    #
    # a = vect_norm(np.array(a).astype("float"))
    # b = 1-vect_norm(np.array(b).astype("float"))
    # b = vect_norm(b)
    #
    #
    # #dist = 1- np.linalg.norm(a - b, ord = 1)*2
    #
    # dist = 1-np.sum(np.abs(a-b))*2
    #
    # return dist

    dentada = np.sum(b)

    a = 1-vect_norm(a)
    b = vect_norm(b)
    #
    # dist = np.linalg.norm(a - b, ord=1) - 1

    dist = (1 -np.sum(np.abs(a-b))*difficulty)*3

    return dist


def get_ratio(color):
    color = color.astype(float)
    color_sum = np.sum(color)

    if color_sum !=0:
        cr_ratio = color/color_sum

    else:
        cr_ratio = np.array([0,0,0])

    return cr_ratio

def vect_norm(v):
    v = np.array(v).astype("float")
    if v.max() >0:
        v /=v.max()
    return v


def calculadentada(valor):
    bitesize = 10
    valor_sum = np.sum(valor)
    if valor_sum != 0:
        valor_norm = valor / valor_sum
        valor_subtracted = valor - valor_norm * bitesize

        valor_clipped = np.clip(valor_subtracted, 0, 100000)
        valor_excess = valor_subtracted - valor_clipped
        valor_updated = valor_subtracted - valor_excess

        dentada = valor - valor_updated

        return dentada
    else:

        return np.array([0, 0, 0])
