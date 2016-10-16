from Distributions import uniforme_discreta
from Distributions import bernoulli

def seguentVehicle():
    return bernoulli(.15, 'moto', 'cotxe')
    
def tempsDipositMoto():
    return erlang2(3)
    
def erlang2(u):
    
    