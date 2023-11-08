# -*- coding: utf-8 -*-
"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    3. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva el máximo y el mínimo de dichos valores, así como sus respectivas posiciones.
Solicitar N por teclado y mostrar el resultado por pantalla.
"""

#Entrada de datos
n = int(input("Introduce un número: "))

#Crear lista
lista = []
for i in range(1, n+1):
    lista.append(i)

#Función 1
def min_max(lista):
    minimo = lista[0]
    maximo = lista[0]
    for i in lista:
        if i < minimo:
            minimo = i
        if i > maximo:
            maximo = i
    return minimo, maximo

#Función 2
def min_max2(lista):
    return min(lista), max(lista)

#Salida de datos
print("El mínimo y el máximo de la lista son: ", min_max(lista))
print("El mínimo y el máximo de la lista son: ", min_max2(lista))