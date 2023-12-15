# -*- coding: utf-8 -*-
import random
import vrep
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob
import parametros as p

"""
    Leemos datos de laser, los mostramos con matplot y los salvamos a un fichero JSON
    Importante: La escena tiene que estar ejecutándose en el simulador (Usar botón PLAY)
"""
def main(src):
    str_objeto = ""
    ficheroTTT = ""
    z = 0

    distancia_inicial = 0
    # mostramos el directorio de trabajo y vemos si existe el dir para salvar los datos
    print("Directorio de trabajo inicial: ", os.getcwd())

    # Cambiar directorio de trabajo
    directorio = src.split("/")[0]
    fichero = src.split("/")[1]

    parte_inicial_fich = fichero[:5]
    parte_final_fich = fichero[-10:-5]
    print(parte_inicial_fich, parte_final_fich)

    #Ajustamos el objeto
    if parte_inicial_fich == "enPie":
        str_objeto = "Bill#0" #Nombre de la persona de pie
        ficheroTTT = "en_pie.ttt"
    elif parte_inicial_fich == "senta":
        str_objeto = "Bill" #Nombre de la persona sentada
        ficheroTTT = "sentado.ttt"
    elif "cilindroMenor" in fichero:
        str_objeto = "Cylinder0" #Cilindro
        ficheroTTT = "cilindro_menor.ttt"
        z=-0.25
    else:
        str_objeto = "Cylinder"  # Cilindro
        ficheroTTT = "cilindro_mayor.ttt"
        z=-0.25


    #Ajustamos la distancia inicial
    if parte_final_fich == "Cerca":
        minimo = p.val_cerca
        maximo = p.val_media
    elif parte_final_fich == "Media":
        minimo = p.val_media
        maximo = p.val_lejos
    else:
        minimo = p.val_lejos
        maximo = p.val_lejos + 1

    print("Distancia inicial:", distancia_inicial)
    print("Objeto: ", str_objeto)

    os.chdir(directorio)
    print("Cambiando el directorio de trabajo: ", os.getcwd())

    # Guardar la referencia al robot
    _, robothandle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de los motores
    _, left_motor_handle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(p.clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)

    # acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(p.clientID, 'LaserData', vrep.simx_opmode_streaming)

    velocidad = 0  # Variable para la velocidad de los motores, dejamos fijo el robot

    # obtenermos la referencia al str_objeto para moverla

    _, personhandle = vrep.simxGetObjectHandle(p.clientID, str_objeto, vrep.simx_opmode_oneshot_wait)

    # Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(p.clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)

    plt.axis('equal')
    plt.axis([0, 4, -2, 2])

    # Creamos el fichero JSON para guardar los datos del laser
    # usamos diccionarios
    segundos = 0.5
    maxIter = p.val_iteraciones
    iteracion = 1

    cabecera = {"TiempoSleep": segundos,
                "MaxIteraciones": maxIter}

    ficheroLaser = open(fichero, "w")
    print("Creado fichero: ", fichero)



    ficheroLaser.write(json.dumps(cabecera) + '\n')

    seguir = True

    while (iteracion <= maxIter and seguir):
        #Posición del objeto
        x = random.uniform(minimo, maximo)
        y = x/100

        posicion = [x, y, z]

        # Situamos donde queremos a la persona sentada, unidades en metros
        returnCode = vrep.simxSetObjectPosition(p.clientID, personhandle, -1, posicion,
                                                vrep.simx_opmode_oneshot)
        # Cambiamos la orientacion, ojo está en radianes: Para pasar de grados a radianes hay que multiplicar por PI y dividir por 180
        returnCode = vrep.simxSetObjectOrientation(p.clientID, personhandle, -1, [0.0, 0.0, 3.05 - (0.20) * iteracion],
                                                   vrep.simx_opmode_oneshot)

        time.sleep(segundos)  # esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido

        puntosx = []  # listas para recibir las coordenadas x, y z de los puntos detectados por el laser
        puntosy = []
        puntosz = []
        returnCode, signalValue = vrep.simxGetStringSignal(p.clientID, 'LaserData', vrep.simx_opmode_buffer)

        datosLaser = vrep.simxUnpackFloats(signalValue)
        for indice in range(0, len(datosLaser), 3):
            puntosx.append(datosLaser[indice + 1])
            puntosy.append(datosLaser[indice + 2])
            puntosz.append(datosLaser[indice])

        print("Iteración: ", iteracion)
        plt.clf()
        plt.plot(puntosx, puntosy, 'r.')
        if iteracion == 1 or iteracion == maxIter:
            plt.savefig('Plot' + str(iteracion - 1) + '.jpg')
        plt.show()

        # Guardamos los puntosx, puntosy en el fichero JSON
        lectura = {"Iteracion": iteracion, "PuntosX": puntosx, "PuntosY": puntosy}
        # ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura) + '\n')

        # Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image = vrep.simxGetVisionSensorImage(p.clientID, camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype=np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img, 2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # salvo a disco la imagen primera y ultima
        if iteracion == 1 or iteracion == maxIter:
            cv2.imwrite('Iteracion' + str(iteracion - 1) + '.jpg', img)

        # Mostrar frame y salir con "ESC"
        cv2.imshow('Image', img)

        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir = False

        iteracion = iteracion + 1

    # detenemos la simulacion
    vrep.simxStopSimulation(p.clientID, vrep.simx_opmode_oneshot_wait)

    # cerramos las ventanas
    cv2.destroyAllWindows()

    finFichero = {"Iteraciones totales": iteracion - 1}
    ficheroLaser.write(json.dumps(finFichero) + '\n')
    ficheroLaser.close()

    os.chdir('..')
    print("Volviendo al directorio: ", os.getcwd())

    # Copiamos el fichero ttt correspondiente en el directorio
    # os.system("cp " + ficheroTTT + " " + directorio)  # ubuntu
    os.system("copy " + ficheroTTT + " " + directorio)  # windows


