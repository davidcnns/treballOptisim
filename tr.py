from utils import seguentVehicle, tempsDipositMoto, tempsDipositCotxe, llistaArribada


def simulacio():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    
    #comensa l'estat inicial
    inicialitzarVariables()
    

    gestionarEsdeveniment()
    
    
    return 0
    
    
def gestionarEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    
    rellotge = esdeveniment[0][0]
    tipusEsd = esdeveniment[0][1]
    
    if tipusEsd == 'arribada':
        #mirar cua mes curta i afegirse
        if esdeveniment[0][3] == 'cotxe':
            
        elif esdeveniment[0][3] == 'moto':
            
        else:
            print('Algu ha afegit un vehicle no reconegut')
        
    elif tipusEsd == 'surt sortidor':
    
    elif tipusEsd == 'surt caixa':
    
    else:
        print('Algu ha afegit un esdeveniment no possible!!')
    
    
def seguentEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    
    #primer comprova si arriba algu mes
    if llistaArribada[0][0] == rellotge:
        
    
    
def inicialitzarVariables():
    global rellotge
    global SM
    global SC
    global C
    global llistaArribada
    
    SM = []
    SC = []
    C = []
    rellotge = 0
    llistaArribada = llistaArribada()
    
    return 0