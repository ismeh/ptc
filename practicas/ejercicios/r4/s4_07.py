"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    7. Usando el módulo “random” genera dos listas de N y M números enteros aleatorios entre 1 y 10 e
implementa una función que devuelva una tercera lista que represente la intersección de las dos
primeras. Los valores deben estar ordenados en orden ascendente. Solicitar N y M por teclado y
mostrar el resultado por pantalla.
"""
import random
RAND_INF = 1
RAND_SUP = 10
SEMILLA = 0
random.seed(SEMILLA)


def ordenar(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                lista[i], lista[j] = lista[j], lista[i]
    return lista

#Entrada de datos
n = int(input("Introduce un número de elementos: "))
m = int(input("Introduce otro número de elementos: "))

#Crear listas
lista1 = [random.randint(RAND_INF, RAND_SUP) for num in range(n)]
lista2 = [random.randint(RAND_INF, RAND_SUP) for num in range(m)]

#Función 1
def interseccion_ordenada(lista1, lista2):
    lista3 = []
    for num in lista1:
        if num in lista2 and num not in lista3:
            lista3.append(num)
    ordenar(lista3)
    return lista3

#Función 2
#Usando set
def interseccion_ordenada2(lista1, lista2):
    interseccion = list(set([num for num in lista1 if num in lista2]))
    interseccion.sort()
    return interseccion

#Función 3 - Usando solo listas
def interseccion_ordenada3(lista1, lista2):
    lista3 = []
    for num in lista1:
        if num in lista2 and num not in lista3:
            lista3.append(num)
    lista3.sort()
    return lista3

#Salida de datos
print("Lista 1: ", lista1)
print("Lista 2: ", lista2)
print("Lista intersección: ", interseccion_ordenada(lista1, lista2))
print("Lista intersección: ", interseccion_ordenada2(lista1, lista2))
print("Lista intersección: ", interseccion_ordenada3(lista1, lista2))