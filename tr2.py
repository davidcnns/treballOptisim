# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:55:12 2016

@author: David
"""

from utils import seguentVehicle, tempsDipositMoto, tempsDipositCotxe, llistaArribada
from utils import tempsDipositVehicle
import sys


def simulacio():
    global rellotge
    global SM
    global SC
    global C        #True si caixa esta lliure, false si algu esta a caixa
    global esdeveniment
    global lSC
    global lSM
    
    
    #comensa l'estat inicial
    inicialitzarVariables()
    
    #Executa cada esdeveniment fins a finalitzar la cua d'esdeveniments
    #la cua d'esdeveniments no pot ser infinita
    while len(esdeveniment) > 0:
        #Agafar seguent estat de l'esdeveniment
        rellotge = esdeveniment[0][0]
        
        #Gestionar un esdeveniment
        gestionarEsdeveniment()
        
    #Aqui caldria imprimir la informacio util

    return 0
    
    
def gestionarEsdeveniment():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global lSC
    global lSM
    
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
            print('ln76')
            lST, ST, index = agafarCuaVehicle(infVeh)
            #Evitar que ningu mes entri a caixa
            C = False
            #Guardar info de quan entra a caixa
            infVeh[3] = rellotge
            #Guardar info de quan sortira de caixa
            infVeh[4] = rellotge + 2
            #Actualitzar llista on esta el vehicle
            print('DOING SOMETHINNNNNGGG:    '+str(index))
            print(SM)
            print(SC)
            ST[index] = infVeh
            print(SM)
            print(SC)
            #Crear nou esdeveniment
            esdeveniment.append([infVeh[4], 'sortir caixa', infVeh])
        #else:
            #Esperar-se per anar a caixa
    
    elif esd[1] == 'sortir caixa':
        #Lliurar caixa
        C = True
        
        #Agafar info del cotxe que surt
        print('ln94')
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
        ST.pop(index)
        
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
            print('ln137')
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
        
    return 0
    
def inicialitzarVariables():
    global rellotge
    global SM
    global SC
    global C
    global esdeveniment
    global lSC
    global lSM
    
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
    print(info)
    print('Cua SC')
    print(SC)
    print('Cua SM')
    print(SM)
    sys.exit('error: no entra be a agafarCuaVehicle')
    
    

    