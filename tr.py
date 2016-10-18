from utils import seguentVehicle, tempsDipositMoto, tempsDipositCotxe, llistaArribada


def simulacio():
    global rellotge
    global SM
    global SC
    global C        #True si caixa esta lliure, false si algu esta a caixa
    global esdeveniment
    global lenSC
    global lenSM
    global params
    
    
    #comensa l'estat inicial
    inicialitzarVariables()
    params[0] = len(esdeveniment)
    while len(esdeveniment) > 0:
        gestionarEsdeveniment()
        
    
    print('Ha acabat')
    print(rellotge)
    print('Longituds:')
    print(len(SC))
    print(len(SM))
    print('Num veh: ' + str(params[0]) + '  Num caix: ' + str(params[1]))
    return 0
    
    
def gestionarEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global params
    
    rellotge = esdeveniment[0][0]
    tipusEsd = esdeveniment[0][1]
    
    if tipusEsd == 'arribada':
        #mirar cua mes curta i afegirse
        if esdeveniment[0][2] == 'cotxe':
            #si hi ha espai per a omplir el diposit, notifica quan acaba
            if len(SC) < lenSC:
                #actualitza el temps de l'activitat
                esdeveniment[0][0] = rellotge + tempsDipositCotxe()
                #Afegeix esdeveniment de acabar
                esdeveniment.append([esdeveniment[0][0],
                                    'diposit ple', 'cotxe', SC, len(SC)])
                SC.append([esdeveniment[0][0], 'cotxe'])
            else:
                SC.append([0, 'cotxe'])
            esdeveniment.pop(0)
            
        elif esdeveniment[0][2] == 'moto':
            if len(SM)<=len(SC):
                if len(SM) < lenSM:
                    
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append([esdeveniment[0][0], 
                                        'diposit ple', 'moto', SM, len(SM)])
                    
                SM.append([esdeveniment[0][0], 'moto'])
                esdeveniment.pop(0)
            else:
                if len(SC) < lenSC:
                    esdeveniment[0][0] = rellotge + tempsDipositMoto()
                    
                    esdeveniment.append([esdeveniment[0][0],
                                        'diposit ple', 'moto', SC, len(SC)])
                SC.append([esdeveniment[0][0], 'moto'])
                esdeveniment.pop(0)
        else:
            print('Algu ha afegit un vehicle no reconegut')
    elif tipusEsd == 'diposit ple':
        if C==True:
            C = False
            
            if esdeveniment[0][3] == SC:
                lenNe = lenSC
            else:
                lenNe = lenSM
            cotxeAcaixa = rellotge + 1
            index = 0
            for i in range(lenNe-1):
                if i < len(esdeveniment[0][3]) and cotxeAcaixa > esdeveniment[0][3][i][0]:
                    cotxeAcaixa = esdeveniment[0][3][i][0]
                    index = i
            #perque hi ha aquest if aqui?
            if len(esdeveniment[0][3]) > 0:
                   esdeveniment.append([rellotge+2,'surt caixa',
                                       esdeveniment[0][2], esdeveniment[0][3], index])
        esdeveniment.pop(0)
        
    elif tipusEsd == 'surt caixa':
        
        params[1] +=1;
        esdeveniment[0][3].pop(esdeveniment[0][4])
        
        if esdeveniment[0][3] == SM:
            if len(SM) >= lenSM and SM[lenSM-1][0] == 0:
                esdeveniment.append([rellotge+tempsDipositMoto(),
                                    'diposit ple', 'moto', SM,
                                    min(lenSM-1, len(SM))])
        else:
            if len(SC) >= lenSC and SC[lenSC-1][0] == 0:
                if SC[lenSC-1][1] == 'moto':
                    esdeveniment.append([rellotge+tempsDipositMoto(),
                                        'diposit ple', 'moto', SC,
                                        min(lenSC-1, len(SC))])
                else:
                    esdeveniment.append([rellotge+tempsDipositCotxe(),
                                        'diposit ple', 'cotxe', SC, 
                                        min(lenSC-1, len(SC))])
        
        cotxeAcaixa = [rellotge, 'notFound']
        llista = []
        for i in range(lenSC-1):
            if i < len(SC) and cotxeAcaixa[0] > SC[i][0]:
                cotxeAcaixa = SC[i]
                llista = [SC, i]
        for i in range(lenSM-1):
            if i < len(SM) and cotxeAcaixa[0] > SM[i][0]:
                cotxeAcaixa = SM[i]
                llista = [SM, i]
        C = True
        if cotxeAcaixa[1] != 'notFound':
            C = False
            esdeveniment.append([rellotge+2, 'surt caixa', cotxeAcaixa[1],
                                llista[0], llista[1]])
        esdeveniment.pop(0)
    else:
        print('Algu ha afegit un esdeveniment no possible!!')
    esdeveniment = sorted(esdeveniment, key =  lambda esdeveniment: esdeveniment[0])
    
    return 0
    
def inicialitzarVariables():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global lenSC
    global lenSM
    global params
    
    params = [0,0]
    
    lenSC = 3
    lenSM = 2
    SM = []
    SC = []
    C = True
    rellotge = 0
    esdeveniment = llistaArribada()
    
    return 0