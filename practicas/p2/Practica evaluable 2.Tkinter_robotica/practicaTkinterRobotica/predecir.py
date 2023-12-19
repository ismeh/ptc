# -*- coding: utf-8 -*-

import os
import pickle
import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import parametros as p
import agrupar as agr
import caracteristicas as car

import vrep

def punto_medio_clusteres(cluster1, cluster2):
    x1 = np.mean(cluster1["PuntosX"])
    y1 = np.mean(cluster1["PuntosY"])
    x2 = np.mean(cluster2["PuntosX"])
    y2 = np.mean(cluster2["PuntosY"])

    punto_medio_x = (x1 + x2) / 2
    punto_medio_y = (y1 + y2) / 2

    return [punto_medio_x, punto_medio_y]

def distancia_entre_clusters(cluster1, cluster2):
    min_dist = np.inf
    for i in range(len(cluster1["PuntosX"])):
        for j in range(len(cluster2["PuntosX"])):
            p1 = [cluster1["PuntosX"][i], cluster1["PuntosY"][i]]
            p2 = [cluster2["PuntosX"][j], cluster2["PuntosY"][j]]
            dist = car.distancia_euclidea(p1, p2)
            if dist < min_dist:
                min_dist = dist

    return min_dist



def main():
    # Si no existe el directorio /prediccion, lo creamos
    if not os.path.exists("prediccion"):
        os.mkdir("prediccion")

    # Nos colocamos en el directorio /prediccion
    os.chdir("prediccion")

    # Guardar la referencia al robot
    _, robothandle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de los motores
    _, left_motor_handle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle = vrep.simxGetObjectHandle(p.clientID, 'Pioneer_p3dx_rightMotor',
                                                     vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(p.clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)

    # acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(p.clientID, 'LaserData', vrep.simx_opmode_streaming)

    velocidad = 0  # Variable para la velocidad de los motores, dejamos fijo el robot

    # Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(p.clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)

    # listas para recibir las coordenadas x, y z de los puntos detectados por el laser
    puntos_agrupados = []
    puntos_x = []
    puntos_y = []

    returnCode, signalValue = vrep.simxGetStringSignal(p.clientID, 'LaserData', vrep.simx_opmode_buffer)
    datosLaser = vrep.simxUnpackFloats(signalValue)

    for indice in range(0, len(datosLaser), 3):
        puntos_x.append(datosLaser[indice + 1])
        puntos_y.append(datosLaser[indice + 2])
        puntos_agrupados.append((datosLaser[indice + 1], datosLaser[indice + 2]))

    # Cálculo los clusters para los puntos de la iteración
    clusters = agr.agrupacion_por_distancia_salto(puntos_agrupados, p.val_umbralDistancia)

    # Cálculo de las características de los clusters
    caracteristicas = []
    for idx in range(len(clusters)):
        clusters[idx] = {
            "PuntosX": [punto[0] for punto in clusters[idx]],
            "PuntosY": [punto[1] for punto in clusters[idx]]
        }
        fila = []
        fila.append(car.calcular_perimetro(clusters[idx]))
        fila.append(car.calcular_profundidad(clusters[idx]))
        fila.append(car.calcular_anchura(clusters[idx]))
        caracteristicas.append(fila)

    carDataF = pd.DataFrame(caracteristicas, columns=['perimetro', 'profundidad', 'anchura'])

    # Leemos el clasificador
    with open("../clasificador.pkl", "rb") as archivo:
        clasificador = pickle.load(archivo)

    # Calculo la predicción
    prediccion=clasificador.predict(carDataF)
    print(f"Predicción ({len(prediccion)}): ", prediccion)

    # Gráfica de predicción
    # Dibujamos los clusters. En rojo los que son piernas y en azul los que no.
    plt.clf()
    plt.axis('tight')
    plt.axis([1, 3.4, -2.15, 2.15])

    label = ["No pierna (0)", "Pierna (1)", "Punto medio"]
    color = ["b.", "r.", "g."]
    
    piernas = []
    no_piernas = []
    pm = []
    
    for i in range(len(carDataF)):
        puntos_cluster = [clusters[i]["PuntosX"], clusters[i]["PuntosY"]]

        if prediccion[i] == 1:
            piernas.append(puntos_cluster)

        else:
            no_piernas.append(puntos_cluster)

        plt.plot(puntos_cluster[0], puntos_cluster[1], color[prediccion[i]])

        # Comprobamos la distancia con los otros clústeres
        for j in range(i + 1, len(carDataF)):
            cluster2 = clusters[j]
            dist = distancia_entre_clusters(clusters[i], cluster2)
            if dist < 0.2:
                # Calculamos el punto medio y lo pintamos en verde
                punto_medio = punto_medio_clusteres(clusters[i], cluster2)
                plt.plot(punto_medio[0], punto_medio[1], color[2])
                pm.append(punto_medio)
                
    # Guardamos la imagen como predecir.jpg
    print("Volviendo al directorio anterior: ", os.getcwd())
    
    # generar leyenda
    plt.plot(no_piernas[0][0], no_piernas[0][1], 'b.', label=label[0])
    plt.plot(piernas[0][0], piernas[0][1], 'r.', label=label[1])

    plt.plot(pm[0][0], pm[0][1], 'g.', label=label[2])
    plt.legend(loc='upper left')

    plt.savefig("predecir.jpg")
    plt.show()

    # Volvemos al directorio padre
    os.chdir("..")