"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    2. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva una lista con los valores impares y el número de dichos valores. Solicitar N por
teclado y mostrar el resultado por pantalla.
"""

#Entrada de datos
n = int(input("Introduce un número: "))

#Crear lista
lista = []
for i in range(1, n+1):
    lista.append(i)

#Función 1
def impares(lista):
    impares = []
    for i in lista:
        if i % 2 != 0:
            impares.appenwd(i)
    return impares, len(impares)

#Función 2
def impares2(lista):
    impares = [impar for impar in lista if impar % 2 != 0]
    return impares, len(impares)

#Salida de datos
res = impares(lista)
print("La lista de impares es: ", res[0], " y tiene ", res[1], " elementos")
res = impares2(lista)
print("La lista de impares es: ", res[0], " y tiene ", res[1], " elementos")