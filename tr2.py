# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:55:12 2016

@author: David
"""

from utils import seguentVehicle, tempsDipositMoto, tempsDipositCotxe, llistaArribada
from utils import tempsDipositVehicle
import sys


def mitjanaSimulacio(quant):
    
    avTotTime = [0,0,0]
    avQueTime = [0,0,0]
    avQue2Time = [0,0,0]
    avFinTime = 0
    
    file = open('ResultatsSim.csv', 'w')
    #Queue1 es la cua per omplir el diposit
    #Queue2 es la cua per anar a caixa
    file.write('Queue1,Queue2,Total Time,Finish Time\n')
    
    for i in range(quant):
        qt, q2t, tt, ft = simulacio()
        for a in range(3):
            avTotTime[a] += tt[a]/quant
            avQueTime[a] += qt[a]/quant
            avQue2Time[a] += q2t[a]/quant
            
        file.write(str(qt[1])+','+str(q2t[1])+','+
                   str(tt[1])+','+str(ft)+'\n')
        avFinTime += ft/quant
        
    file.close()
    
    print(avQue2Time)
    print('List of results of ' + str(quant) + ' simulations:')
    print(' -Average gas queue wait time: ' + str(avQueTime[1]))
    print(' -Average pay queue wait time: ' + str(avQue2Time[1]))
    print(' -Average total time:          ' + str(avTotTime[1]))
    print(' -Average closing time:        ' + str(avFinTime))
    print('')
    print(' -Min gas queue wait time:     ' + str(avQueTime[0]))
    print(' -Min pay queue wait time:     ' + str(avQue2Time[0]))
    print(' -Min total time:              ' + str(avTotTime[0]))
    print('')
    print(' -Max gas queue wait time:     ' + str(avQueTime[2]))
    print(' -Max pay queue wait time:     ' + str(avQue2Time[2]))
    print(' -Max total time:              ' + str(avTotTime[2]))
    
    return 0

def simulacio():
    global rellotge
    global SM
    global SC
    global C        #True si caixa esta lliure, false si algu esta a caixa
    global esdeveniment
    global lSC
    global lSM
    global infoFinal
    
    #comensa l'estat inicial
    inicialitzarVariables()
    
    #Executa cada esdeveniment fins a finalitzar la cua d'esdeveniments
    #la cua d'esdeveniments no pot ser infinita
    while len(esdeveniment) > 0:
        #Agafar seguent estat de l'esdeveniment
        rellotge = esdeveniment[0][0]
        
        #Gestionar un esdeveniment
        gestionarEsdeveniment()
        
    #Imprimir informacio util
    averageTotalTime = [infoFinal[-1][4],0,0]
    averageWaitTime =  [infoFinal[-1][4],0,0]
    averageWaitTime2 = [infoFinal[-1][4],0,0]
    
    for temp in infoFinal:
        averageWaitTime[1] += temp[7]
        averageWaitTime2[1] += temp[8]
        averageTotalTime[1] += temp[9]
    
    averageWaitTime[1] /= len(infoFinal)
    averageWaitTime2[1] /= len(infoFinal)
    averageTotalTime[1] /= len(infoFinal)
    
    infoFinal = sorted(infoFinal, key =  lambda infoFinal: infoFinal[7])
    averageWaitTime[0] = infoFinal[0][7]
    averageWaitTime[2] = infoFinal[-1][7]
    
    infoFinal = sorted(infoFinal, key =  lambda infoFinal: infoFinal[8])
    averageWaitTime2[0] = infoFinal[0][8]
    averageWaitTime2[2] = infoFinal[-1][8]
    
    infoFinal = sorted(infoFinal, key =  lambda infoFinal: infoFinal[9])
    averageTotalTime[0] = infoFinal[0][9]
    averageTotalTime[2] = infoFinal[-1][9]
    
    #print('Av. Total wait time: ' + str(averageTotalTime))
    #print('Av. Que wait time: ' + str(averageWaitTime))
    infoFinal = sorted(infoFinal, key =  lambda infoFinal: infoFinal[4])
    return averageWaitTime, averageWaitTime2, averageTotalTime, infoFinal[-1][4]
    
    
def gestionarEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global lSC
    global lSM
    global infoFinal
    
    #Agafar esdeveniment
    esd = esdeveniment.pop(0)
    
    #Agafar info del cotxe de l'esdeveniment
    infVeh = esd[2]

    if esd[1] == 'arribada':
        #Assignar una cua al vehicle (en funcio del tipus i de les cues)
        lST, ST = agafarCuaCorresponent(infVeh)
        
        #Mirar si el vehicle pot comensar a omplir el diposit
        if lST > len(ST):   #si que pot
            #Guardar info de quan ha comensat a omplir el diposit
            infVeh[1] = rellotge
            #Guardar info de quan acabara d'omplir el diposit
            infVeh[2] = rellotge + tempsDipositVehicle(infVeh)
            #Afegir l'esdeveniment
            esdeveniment.append([infVeh[2],'diposit ple', infVeh])
        #else:
            #no fa re, el seguent cotxe que surti mirara si algu ha de omplir el diposit
            
        #Afegir el vehicle a la cua
        ST.append(infVeh)
        
    elif esd[1] == 'diposit ple':
        if C == True:
            lST, ST, index = agafarCuaVehicle(infVeh)
            #Evitar que ningu mes entri a caixa
            C = False
            #Guardar info de quan entra a caixa
            infVeh[3] = rellotge
            #Guardar info de quan sortira de caixa
            infVeh[4] = rellotge + 2
            #Actualitzar llista on esta el vehicle
            ST[index] = infVeh
            #Crear nou esdeveniment
            esdeveniment.append([infVeh[4], 'sortir caixa', infVeh])
        #else:
            #Esperar-se per anar a caixa
    
    elif esd[1] == 'sortir caixa':
        #Lliurar caixa
        C = True
        
        #Agafar info del cotxe que surt
        lST, ST, index = agafarCuaVehicle(infVeh)
        
        ##################
        #mirar si algu ha de começar a omplir el diposit
        if lST < len(ST):
            #Copiar llista ST per modificarla més facilment
            vehicle = ST[lST]

            #Indicar quan acabara d'omplir el diposit
            t = rellotge + tempsDipositVehicle(vehicle)
            
            #Guardar info de quan ha comensat a omplir el diposit
            vehicle[1] = rellotge
            
            #Guardar info de quan acabara d'omplir el diposit
            vehicle[2] = t
            
            #Actualitzar llista ST (SC o SM)
            ST[lST] = vehicle
            
            #Afegir l'esdeveniment
            esdeveniment.append([t,'diposit ple', vehicle])
        
        ##################
        #Mirar si algu ha de omplir el diposit
        
        #Treure el cotxe de la llista
        temp = ST.pop(index)
        temp += [temp[1]-temp[0], temp[3]-temp[2], temp[4]-temp[0]]
        infoFinal.append(temp)
        
        minim = rellotge
        vehicle = []
        #Mirar si algun vehicle ha acabat de omplir el diposit
        #Comprovar lllista SC
        for veh in SC:
            if 0 != veh[2] < minim:
                minim = veh[2]
                vehicle = veh
        #Comprovar llista SM
        for veh in SM:
            if 0 != veh[2] < minim:
                minim = veh[2]
                vehicle = veh
        
        #Si algun vehicle ha d'anar a caixa ho fa
        if vehicle != []:
            lST2, ST2, index2 = agafarCuaVehicle(vehicle)
            #Evitar que ningu mes entri a caixa
            C = False
            #Guardar info de quan entra a caixa
            vehicle[3] = rellotge
            #Guardar info de quan sortira de caixa
            vehicle[4] = rellotge + 2
            #Actualitzar llista on esta el vehicle
            ST2[index2] = vehicle
            #Crear nou esdeveniment
            esdeveniment.append([vehicle[4], 'sortir caixa', vehicle])
        
        
    else:
        sys.exit('Esdeveniment no possible')
    
    #Ordenar llista de esdeveniments
    esdeveniment = sorted(esdeveniment, key =  lambda esdeveniment: esdeveniment[0])
        
    return 0
    
def inicialitzarVariables():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global lSC
    global lSM
    global infoFinal
    
    #Indicar quants sortidors hi ha a cada cua
    lSC = 3
    lSM = 2
    
    #Indicar que les cues SM i SC son diccionaris
    SM = []
    SC = []
    
    #indicar que caixa esta buida
    C = True
    
    #Crear tots els esdeveniments d'arribada
    esdeveniment = llistaArribada()
    
    #Inicialitzar llista de esdeveniments succeits
    infoFinal = []
    
    return 0



#retorna la longitud de la llista a on es posara i quina es.
def agafarCuaCorresponent(info):
    global SM
    global SC
    
    if info[5] == 'cotxe':
        return lSC,SC
    elif info[5] == 'moto':
        if len(SM)<=len(SC):
            return lSM,SM
        else:
            return lSC,SC
    else:
        sys.exit('error a agafarCuaCorresponent' + info[5])



#retorna longitud de la llista on esta, la llista i la posicio a dins de la llista.
def agafarCuaVehicle(info):
    mat = info[6]
    for i in SC:
        if i[6] == mat:
            return lSC,SC,SC.index(i)
    for i in SM:
        if i[6] == mat:
            return lSM,SM,SM.index(i)
    sys.exit('error: no entra be a agafarCuaVehicle')
    
    

    