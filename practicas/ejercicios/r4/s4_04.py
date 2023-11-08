"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio  (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    4. Usando el módulo “random” genera dos listas de N y M números enteros aleatorios entre 1 y 10 e
implementa una función que devuelva una tercera lista que contenga los números de las dos
primeras listas en orden ascendente sin contener valores repetidos. Solicitar N y M por teclado y
mostrar el resultado por pantalla.
"""

import random
RAND_INF = 1
RAND_SUP = 10
SEMILLA = 0
random.seed(SEMILLA)

def ordenar(lista):
        for i in range(len(lista)):
            for j in range(i+1, len(lista)):
                if lista[i] > lista[j]:
                    lista[i], lista[j] = lista[j], lista[i]
        return lista

#Entrada de datos
n = int(input("Introduce un número: "))
m = int(input("Introduce un número: "))

#Crear listas
lista1 = [random.randint(RAND_INF, RAND_SUP) for num in range(n)]
lista2 = [random.randint(RAND_INF, RAND_SUP) for num in range(m)]

#Función 1
def combina_ordena(lista1, lista2):
    """Genera una tercera lista sin valores repetidos y ordenados de de forma ascendente

    Args:
        lista1 : 
        lista2 : 

    Returns:
        lista3: lista ordenada y sin valores repetidos
    """
    lista3 = []
    for i in lista1:
        if i not in lista3:
            lista3.append(i)
    for i in lista2:
        if i not in lista3:
            lista3.append(i)
    
    lista3 = ordenar(lista3) #Otro modo sería usar lista3.sort()

    return lista3


#Función 2 - Usando un set y sort()
def combina_ordena2(lista1, lista2):
    conjunto = set(lista1 + lista2)
    lista3 = list(conjunto)
    lista3.sort()
    return list(lista3)

    """ Versión con count()
    lista3 = []
    for i in lista1:
        if lista3.count(i) == 0:
            lista3.append(i)
    for i in lista2:
        if lista3.count(i) == 0:
            lista3.append(i)
    """


#Salida de datos
print("lista1: ", lista1, "con ", len(lista1), " elementos")
print("lista2: ", lista2 , "con ", len(lista2), " elementos")
lista3 = combina_ordena(lista1, lista2)
print("La lista combinada y ordenada es: ", lista3, "con ", len(lista3), " elementos")
lista3 = combina_ordena2(lista1, lista2)
print("La lista combinada y ordenada es: ", lista3, "con ", len(lista3), " elementos")
