# -*- coding: utf-8 -*-
"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    5. Partiendo de una lista que contiene a su vez N listas de M enteros, si la consideramos como una
matriz de dimensión NxM, implementar una función que nos devuelva la matriz traspuesta MxN
(intercambiando filas y columnas) que contedrá M listas de N enteros. Solicitar N y M por teclado y
mostrar el resultado por pantalla.
"""

import random
RAND_INF = 1
RAND_SUP = 10
SEMILLA = 0
random.seed(SEMILLA)


#Entrada de datos
n = int(input("Introduce un número de listas: "))
m = int(input("Introduce un número de enteros: "))

#Crear listas
lista = [] #Matrix NxM
for i in range(n):
    lista.append([])
    for j in range(m):
        lista[i].append(random.randint(RAND_INF, RAND_SUP))

def mostrar_matriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])

#Función 1
def traspuesta(matriz):
    traspuesta = []
    for i in range(len(matriz[0])):
        traspuesta.append([])
        for j in range(len(matriz)):
            traspuesta[i].append(matriz[j][i])
    return traspuesta

def traspuesta2(matriz):
    traspuesta = ([[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))])

    return traspuesta

#Salida de datos
print("Matriz original:")
mostrar_matriz(lista)
print("Matriz traspuesta:")
mostrar_matriz(traspuesta(lista))
print("Matriz traspuesta2:")
mostrar_matriz(traspuesta2(lista))
