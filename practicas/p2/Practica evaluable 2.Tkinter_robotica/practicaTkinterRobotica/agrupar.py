import glob
import json
import os
import sys
import parametros as p
from matplotlib import pyplot as plt

import parametros as p

MinPuntos = p.val_minPuntos
MaxPuntos = p.val_maxPuntos
umbralDistancia = p.val_umbralDistancia

puntos = []
clusters = []

def distancia_euclidea(p1, p2):
    return abs((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)

# A esta función le vamos a pasar una iteración del capturar datos (es decir una serie de puntos)
# A partir de esos puntos vamos a ver cuantos clusters podemos calcular
# Es decir está función devuelve una lista de clusters
def agrupacion_por_distancia_salto(puntos, umbralDist):
    clusters = []
    cluster = [puntos[0]]
    puntos_actuales = 0
    for punto in puntos[1:]:
        if (distancia_euclidea(punto, cluster[-1]) < umbralDist) and puntos_actuales < MaxPuntos:
            cluster.append(punto)
            puntos_actuales += 1
        else:
            #Si el cluster tiene suficientes puntos lo añado
            if (puntos_actuales > MinPuntos):
                clusters.append(cluster)
            cluster = []
            cluster.append(punto)
            puntos_actuales = 0

    # Si el cluster tiene suficientes puntos lo añado
    if (puntos_actuales > MinPuntos):
        clusters.append(cluster)

    return clusters

def main():
    # mostramos el directorio de trabajo y leemeos los datos del primero
    print("Directorio de trabajo es: ", os.getcwd()[-p.longitud_output:])

    directorios_pos = sorted(glob.glob("positivo*"))
    directorios_neg = sorted(glob.glob("negativo*"))

    # numDirLecturas = len(listaDir)
    #
    # if (numDirLecturas > 0):
    #     print("Numero de directorios con lecturas: ", numDirLecturas)
    #     print("Leemos solo el primero: ", listaDir[0])
    # else:
    #     sys.exit("Error, no hay directorios con lecturas")

# En cada directorio leemos los datos del fichero JSON y los guardamos en una lista de objetos y calculamos los clusters
    def iterar_directorios(directorios):
        clusters_directorios = []

        if "positivo" in directorios[0]:
            #Crera fichero
            f_clusters = open("clustersPiernas.json", 'w')
        else:
            f_clusters = open("clustersNoPiernas.json", 'w')


        for directorio in directorios:
            objetos = []
            clusters_json = []

            os.chdir(directorio)
            print("Cambiando el directorio de trabajo a: ", os.getcwd()[-p.longitud_output:])

            if len(glob.glob("*.json")) == 0:
                print("No hay ficheros JSON en el directorio: ", directorio)
                os.chdir("..")
                print("Volviendo al directorio anterior: ", os.getcwd())
            else:
                # Leemos el fichero JSON de la captura de datos
                with open(glob.glob("*.json")[0], 'r') as f:
                    for line in f:
                        objetos.append(json.loads(line))

                # cabecera = objetos[0]
                # segundos = cabecera['TiempoSleep']
                # maxIter = cabecera['MaxIteraciones']


                iterTotalesDict = objetos[len(objetos) - 1]

                iterTotales = iterTotalesDict['Iteraciones totales']

                # plt.axis('equal')
                # plt.axis([0, 4, -2, 2])

                #Para cada iteración del json
                for i in range(iterTotales):
                    puntos = []
                    #Agrupo los puntos de una iteración de la captura de datos
                    for j in range(len(objetos[i + 1]['PuntosX'])):
                        puntos.append((objetos[i + 1]['PuntosX'][j], objetos[i + 1]['PuntosY'][j]))

                    # Cálculo los clusters para los puntos de la iteración
                    clusters_it = agrupacion_por_distancia_salto(puntos, umbralDistancia)
                    clusters_json.append(clusters_it)

                #Tras analizar el json del directorio volvemos al directorio padre
                print("Analizado directorio actual")
                os.chdir("..")
                print("Volviendo al directorio anterior: ", os.getcwd())
                clusters_directorios.append(clusters_json)

        num_clus = 1
        for cl_dir in clusters_directorios:
            for cl_it in cl_dir:
                for cl in cl_it:
                    num_puntos = len(cl)
                    puntosX = []
                    puntosY = []
                    for punto in cl:
                        puntosX.append(punto[0])
                        puntosY.append(punto[1])

                    texto = {"numero_cluster": num_clus, "numero_puntos":num_puntos, "PuntosX": puntosX, "PuntosY": puntosY}
                    num_clus += 1
                    f_clusters.write(json.dumps(texto) + '\n')

        f_clusters.close()

        return clusters_directorios

    iterar_directorios(directorios_pos)
    iterar_directorios(directorios_neg)