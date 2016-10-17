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
                esdeveniment.append((esdeveniment[0][0],
                                    'diposit ple', 'cotxe', SC, len(SC)))
            #Afegeix el cotxe a la cua de SC
            SC.append((esdeveniment[0][0], 'cotxe'))
            esdeveniment.pop(0)
            
        elif esdeveniment[0][2] == 'moto':
            if len(SM)<=len(SC):
                if len(SM) < utils.lenSM:
                    
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append((esdeveniment[0][0], 
                                        'diposit ple', 'moto', SM, len(SM)))
                    
                SM.append((esdeveniment[0][0], 'moto'))
                esdeveniment.pop(0)
            else:
                if len(SC) < utils.lenSC:
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append((esdeveniment[0][0],
                                        'diposit ple', 'moto', SC, len(SC)))
                SC.append((esdeveniment[0][0], 'moto'))
                esdeveniment.pop(0)
        else:
            print('Algu ha afegit un vehicle no reconegut')
            
    elif tipusEsd == 'diposit ple':
        if C==True:
            C=False
            esdeveniment.append((rellotge+2,'surt caixa',
                                esdeveniment[0][2], esdeveniment[0][3], ))
            esdeveniment[0][3][0] = edeveniment[0][0]
            esdeveniment[0][3][0] = rellotge+2
        esdeveniment.pop(0)
        
    elif tipusEsd == 'surt caixa':
<<<<<<< HEAD
        C=True
        esdeveniment
=======
        esdeveniment[0][3].pop(esdeveniment[0][4])
        if esdeveniment[0][3] == SM:
            if SM >= lenSM:
                esdeveniment.append((rellotge+tempsDipositMoto(),
                                    'diposit ple', 'moto', SM, lenSM-1))
        else:
            if SC >= lenSC:
                if SC[lenSC-1][1] == 'moto':
                    esdeveniment.append((rellotge+tempsDipositMoto(),
                                        'diposit ple', 'moto', SC, lenSC-1))
                else:
                    esdeveniment.append((rellotge+tempsDipositCotxe(),
                                        'diposit ple', 'cotxe', SC, lenSC-1))
        cotxeAcaixa = (rellotge, 'notFound')
        for i in range(lenSC-1):
            if cotxeAcaixa[0] > SC[i][0]:
                cotxeAcaixa = SC[i] + (SM, i)
        for i in range(lenSM-1):
            if cotxeAcaixa[0] > SM[i][0]:
                cotxeAcaixa = SM[i] + (SM, i)
        C = True
        if cotxeAcaixa[1] != 'notFound':
            C = False
            esdeveniment.append((rellotge+2, 'surt caixa', cotxeAcaixa[1],
                                cotxeAcaixa[2], cotxeAcaixa[3]))
>>>>>>> 938bc45c60b1e7afd5fbf23d464709e466b52273
        
    else:
        print('Algu ha afegit un esdeveniment no possible!!')
        
    esdeveniment = sorted(esdeveniment, key = lambda esdeveniment:esdeveniment[0])
    
    
def inicialitzarVariables():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    
    SM = []
    SC = []
    C = []
    rellotge = 0
    esdeveniment = llistaArribada()
    
    return 0