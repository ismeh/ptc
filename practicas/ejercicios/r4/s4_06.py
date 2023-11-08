# -*- coding: utf-8 -*-
"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    6. Solicitar un número entero N por teclado e implentar una función que devuelva una lista con la
descomposición en factores primos de N. Mostrar el resultado por pantalla.
"""
#Entrada de datos
n = int(input("Introduce un número a descomponer: "))

#Función 1
def descomponer(n):
    lista = []
    i = 2
    while n > 1:
        if n % i == 0:
            lista.append(i)
            n = n / i
        else:
            i = i + 1
    return lista

#Salida de datos
print("La descomposición en factores primos de", n, "es:", descomponer(n))