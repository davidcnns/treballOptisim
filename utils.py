from Distribucions import uniforme_discreta
from Distribucions import bernoulli
import numpy

def seguentVehicle():
    return bernoulli(.15, 'moto', 'cotxe')
    
def tempsDipositMoto():
    return erlang2(3)
    
def tempsDipositCotxe():
    return 
    
def erlang2(u):
    
    return 0
    
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