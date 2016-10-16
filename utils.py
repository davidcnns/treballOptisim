from Distribucions import uniforme_discreta
from Distribucions import bernoulli
import numpy
import math

def seguentVehicle():
    return bernoulli(.15, 'moto', 'cotxe')
    
def tempsDipositMoto():
    return erlang2(3)
    
def tempsDipositCotxe():
    return normalTrunc(8,2,5,13)
    
def erlang2(u):
    k=0
    y=1
    while k<2:
        y=y*numpy.random.random()
        k=k+1
    x=(-u/2)*math.log(y)
    return x
    
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