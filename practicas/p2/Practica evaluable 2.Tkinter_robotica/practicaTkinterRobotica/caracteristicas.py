# -*- coding: utf-8 -*-
import json
import math
import os
import parametros as p

def distancia_euclidea(p1, p2):
    return abs((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)

def calcular_perimetro(cluster):
    perimetro = 0
    for i in range(len(cluster['PuntosX']) - 1):
        p1 = (cluster['PuntosX'][i], cluster['PuntosY'][i])
        p2 = (cluster['PuntosX'][i+1], cluster['PuntosY'][i+1])
        perimetro += distancia_euclidea(p1, p2)
    return perimetro

def calcular_anchura(cluster):
    p1 = (cluster['PuntosX'][0], cluster['PuntosY'][0])
    p2 = (cluster['PuntosX'][-1], cluster['PuntosY'][-1])
    return distancia_euclidea(p1, p2)
def calcular_profundidad(cluster):
    prof_max = 0

    for i in range(len(cluster['PuntosX'])-1):
        p1 = (cluster['PuntosX'][i], cluster['PuntosY'][i])
        p2 = (cluster['PuntosX'][i+1], cluster['PuntosY'][i+1])
        prof_max = max(prof_max, distancia_euclidea(p1, p2))

    return prof_max

def generar_caracteristicas(input_file, output_file, es_pierna):
    clusters = []
    with open(input_file, 'r') as f:
        for line in f:
            clusters.append(json.loads(line))

    caracteristicas = []

    for i, cluster in enumerate(clusters, 1):
        perimetro = calcular_perimetro(cluster)
        profundidad = calcular_profundidad(cluster)
        anchura = calcular_anchura(cluster)

        caracteristicas_cluster = {
            "numero_cluster": i,
            "perimetro": perimetro,
            "profundidad": profundidad,
            "anchura": anchura,
            "esPierna": es_pierna
        }

        caracteristicas.append(caracteristicas_cluster)

    with open(output_file, 'w') as f:
        for cluster in caracteristicas:
            f.write(json.dumps(cluster) + '\n')

def combinar_ficheros(input_file1, input_file2, output_file):
    clusters1 = []
    with open(input_file1, 'r') as f:
        for line in f:
            clusters1.append(json.loads(line))

    clusters2 = []
    with open(input_file2, 'r') as f:
        for line in f:
            clusters2.append(json.loads(line))

    clusters = clusters1 + clusters2

    with open(output_file, 'w') as f:
        for cluster in clusters:
            linea = str(cluster['perimetro']) + ',' + str(cluster['profundidad']) + ',' + str(cluster['anchura']) + ',' + str(cluster['esPierna'])
            f.write(linea + '\n')
def main():
    print("Directorio de trabajo es: ", os.getcwd()[-p.longitud_output:])

    # Generar características para las piernas
    generar_caracteristicas("clustersPiernas.json", "caracteristicasPiernas.dat", es_pierna=1)

    # Generar características para no piernas
    generar_caracteristicas("clustersNoPiernas.json", "caracteristicasNoPiernas.dat", es_pierna=0)
    print("Se han generado las características de los clusters")

    # Combinar los ficheros de características
    combinar_ficheros("caracteristicasPiernas.dat", "caracteristicasNoPiernas.dat", "piernasDataset.csv")
    print("Se han combinado los ficheros de características en el fichero 'piernasDataset.csv'")