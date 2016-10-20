from Distribucions import uniforme_discreta
from Distribucions import bernoulli
import numpy
import math

def tempsDipositVehicle(vehicle):
    if vehicle[5] == 'cotxe':
        return tempsDipositCotxe()
    elif vehicle[5] == 'moto':
        return tempsDipositMoto()

#Defineix de forma aleatoria el quin tipus de vehicle sera el seguent
def seguentVehicle():
    return bernoulli(.15, 'moto', 'cotxe')

#Obtenir el temps que triga en omplir el diposit la moto
def tempsDipositMoto():
    return erlang2(3)

#Obtenir el temps que triga en omplir el diposit el cotxe    
def tempsDipositCotxe():
    return normalTrunc(8,2,5,13)

#retorna una variable aleatoria amb distribucio erlang-2 i mitjana u
def erlang2(u):
    k=0
    y=1
    while k<2:
        y=y*numpy.random.random()
        k=k+1
    x=(-u/2)*math.log(y)
    return x

#retorna una variable aleatoria amb una distribucio normal de mitja u, sigma sig
# i truncada pels valors vmin i vmax
def normalTrunc(u, sig, vmin, vmax):
    randomVal = numpy.random.normal(u, sig)
    count = 0
    while count < 1000000:
        if vmin <= randomVal <= vmax:
            return randomVal
        else:
            randomVal = numpy.random.normal(u, sig)
        count += 1
    return u

#retorna una variable aleatoria amb una distribucio exponencial de mitjana u
def exponencial(u):
        y=numpy.random.random()
        x=(-u)*math.log(y)
        return x    
        
#genera tots els esdeveniments d'arribada durant el dia
def llistaArribada():
    t = 0
    llista = []
    k = 0
    t = exponencial(5)
    while t< 10:#16*60:
        #afegeix cotxe a la llista
        llista.append([t, 'arribada', [t, 0,0,0,0, seguentVehicle(), 'id' + str(k)]])
        
        #incrementa temps i matricula del vehicle
        t += exponencial(5)
        k += 1
    #retorna la llista amb tots els esdeveniments ja ordenats
    return llista
