# -*- coding: utf-8 -*-
"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    8. Realizar un programa que muestre un menú de opciones al usuario con las siguientes operaciones
sobre una lista que inicialmente está vacía: 1) Insertar un entero positivo (debe insertarlo en orden
ascendente), 2) Eliminar un valor de la lista dado el entero positivo, 3) Eliminar un valor dada su
posición, 4) Salir. Después de cada operación se debe siempre mostrar al usuario el estado de la
lista y se deben controlar las posibles situaciones de error informando al usuario de dicho error y
volviendo a solicitar la entrada correspondiente.
"""
def insertar(lista):
    numero = (input("Introduce un número a insertar: "))

    def comprobaciones(numero):
        continuar = True
        if not numero.isdigit():
            print("Debe introducir un número entero positivo")
            continuar = False
        else:
            numero = int(numero)
            if len(lista) > 1:
                if lista[len(lista) - 1] > numero:
                    print("Debe introducir un número mayor que el último de la lista,", lista[len(lista) - 1])
                    continuar = False
        return continuar

    while (comprobaciones(numero) == False):
        numero = (input("Introduce un número a añadir: "))

    lista.append(int(numero))

def eliminar_valor(lista):
    numero = (input("Introduce un número a eliminar: "))

    def comprobaciones(numero):
        continuar = True
        if len(lista) == 0:
            print("La lista está vacía")
            continuar = False
        if continuar:
            if not numero.isdigit():
                print("Debe introducir un número entero positivo")
                continuar = False
            else:
                numero = int(numero)
                if numero not in lista:
                    print("El número no está en la lista")
                    continuar = False
        return continuar

    while(comprobaciones(numero) == False):
        numero = (input("Introduce un número a eliminar: "))

    lista.remove(int(numero))

def eliminar_posicion(lista):
    posicion = (input("Introduce una posición a eliminar: "))
    lista_vacia = False

    def comprobaciones(posicion):
        continuar = True
        if len(lista) == 0:
            print("La lista está vacía")
            continuar = False
            lista_vacia = True

        if continuar:
            if not posicion.isdigit():
                print("Debe introducir un número entero positivo")
                continuar = False
            else:
                posicion = int(posicion)
                if posicion >= len(lista):
                    print("La posición no está en la lista")
                    continuar = False
        return continuar

    while (comprobaciones(posicion) == False and lista_vacia == True):
        posicion = (input("Introduce un número a eliminar: "))

    if lista_vacia == False:
        lista.pop(int(posicion))
def menu(lista):
    def relanzar(funcion, lista):
        funcion(lista)
        print(lista)
        menu(lista)
    print("1) Insertar un entero positivo")
    print("2) Eliminar un valor de la lista")
    print("3) Eliminar un valor dada su posición")
    print("4) Salir")
    opcion = int(input("Introduce una opción: "))

    if opcion == 1:
        relanzar(insertar,lista)
    elif opcion == 2:
        relanzar(eliminar_valor,lista)
    elif opcion == 3:
        relanzar(eliminar_posicion,lista)
    elif opcion == 4:
        print("Adiós")

lista = []
menu(lista)
