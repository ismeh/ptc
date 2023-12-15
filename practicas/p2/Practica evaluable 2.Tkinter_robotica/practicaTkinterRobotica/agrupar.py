import glob
import json
import os
import sys

from matplotlib import pyplot as plt

import parametros as p

MinPuntos = p.val_minPuntos
MaxPuntos = p.val_maxPuntos

puntos = []
clusters = []

def distancia_euclidea_3D(p1, p2):
    return abs((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)**(1/2)

def agrupacion_por_distancia_salto(puntos, clusters, umbralDistancia):
    clusters = []
    cluster = [puntos[0]]
    puntos_actuales = 0
    for punto in puntos[1:]:
        if (distancia_euclidea_3D(punto, cluster[-1]) < umbralDistancia) and puntos_actuales < MaxPuntos:
            cluster.append(punto)
        else:
            if (puntos_actuales > MinPuntos):
                clusters.append(cluster)
            cluster = []
            cluster.append(punto)
            puntos_actuales = 0

    if (puntos_actuales > MinPuntos):
        clusters.append(cluster)

    return clusters

def main():
    # mostramos el directorio de trabajo y leemeos los datos del primero
    print("Directorio de trabajo es: ", os.getcwd())

    directorios_pos = sorted(glob.glob("positivo*"))
    directorios_neg = sorted(glob.glob("negativo*"))

    # numDirLecturas = len(listaDir)
    #
    # if (numDirLecturas > 0):
    #     print("Numero de directorios con lecturas: ", numDirLecturas)
    #     print("Leemos solo el primero: ", listaDir[0])
    # else:
    #     sys.exit("Error, no hay directorios con lecturas")

    def iterar_directorios(directorios):
        os.chdir(directorios[0])
        print("Cambiando el directorio de trabajo a: ", os.getcwd())

        objetos = []

        with open('datosLaser.json', 'r') as f:
            for line in f:
                objetos.append(json.loads(line))

        cabecera = objetos[0]
        segundos = cabecera['TiempoSleep']
        maxIter = cabecera['MaxIteraciones']

        iterTotalesDict = objetos[len(objetos) - 1]

        iterTotales = iterTotalesDict['Iteraciones totales']

        plt.axis('equal')
        plt.axis([0, 4, -2, 2])

        for i in range(iterTotales):
            iteracion = objetos[i + 1]['Iteracion']
            puntosX = objetos[i + 1]['PuntosX']
            puntosY = objetos[i + 1]['PuntosY']

            print("Iteración: ", iteracion)
            plt.clf()
            plt.plot(puntosX, puntosY, 'r.')
            plt.show()

    iterar_directorios(directorios_pos)
    iterar_directorios(directorios_neg)