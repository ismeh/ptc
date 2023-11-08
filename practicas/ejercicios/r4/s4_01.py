# -*- coding: utf-8 -*-
"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    1. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva la suma de dichos valores. Solicitar N por teclado y mostrar el resultado por pantalla.
"""

#Entrada de datos
n = int(input("Introduce un número: "))

#Crear lista
lista = []
for i in range(1, n+1):
    lista.append(i)

#Función 1
def suma_lista(lista):
    suma = 0
    for i in lista:
        suma += i
    return suma

#Función 2
def suma_lista2(lista):
    return sum(lista)

#Salida de datos
print("La suma de los valores de la lista es: ", suma_lista(lista))
print("La suma de los valores de la lista es: ", suma_lista2(lista))

