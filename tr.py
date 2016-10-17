from utils import seguentVehicle, tempsDipositMoto, tempsDipositCotxe, llistaArribada


def simulacio():
    global rellotge
    global SM
    global SC
    global C        #True si caixa esta lliure, false si algu esta a caixa
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
        if esdeveniment[0][2] == 'cotxe':
            #si hi ha espai per a omplir el diposit, notifica quan acaba
            if len(SC) < utils.lenSC:
                #actualitza el temps de l'activitat
                esdeveniment[0][0] = rellotge + tempsDipositCotxe()
                #Afegeix esdeveniment de acabar
                esdeveniment.append([esdeveniment[0][0],
                                    'diposit ple', 'cotxe', SC])
            #Afegeix el cotxe a la cua de SC
            SC.append(esdeveniment.pop(0))
            
        elif esdeveniment[0][2] == 'moto':
            if len(SM)<=len(SC):
                if len(SM) < utils.lenSM:
                    
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append((esdeveniment[0][0], 
                                        'diposit ple', 'moto', SM))
                SM.append(esdeveniment.pop(0))
            else:
                if len(SC) < utils.lenSC:
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append((esdeveniment[0][0],
                                        'diposit ple', 'moto', SC))
                SC.append(esdeveniment.pop(0))    
            
        else:
            print('Algu ha afegit un vehicle no reconegut')
        esdeveniment = sorted(esdeveniment, key = lambda esdeveniment:esdeveniment[0])
    elif tipusEsd == 'diposit ple':
        if C==True:
            C=False
            esdeveniment.append((rellotge+2,'surt caixa',esdeveniment[0][2],esdeveniment[0][3]))
        esdeveniment.pop(0)
        
    elif tipusEsd == 'surt caixa':
        C=True
        esdeveniment
        
    else:
        print('Algu ha afegit un esdeveniment no possible!!')
    
    
def seguentEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    #esdeveniment [(temps de l'esdeveniment,tipus esdeveniment,cotxe/moto,cua on espera)]
    #primer comprova si arriba algu mes
    if llistaArribada[0][0] == rellotge:
        
    esdeveniment=[]
    
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