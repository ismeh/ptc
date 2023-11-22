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

def menu2(lista):
    def imprimir_opciones():
        print("1) Insertar un entero positivo")
        print("2) Eliminar un valor de la lista")
        print("3) Eliminar un valor dada su posición")
        print("4) Salir")

    imprimir_opciones()
    opcion = int(input("Introduce una opción: "))

    while opcion != 4:
        try:
            if opcion == 1:
                num = (input("Introduce un número a insertar: "))
                assert num.isdigit(), "Debe introducir un número entero positivo"
                lista.append(int(num))
            elif opcion == 2:
                assert len(lista) > 0, "La lista está vacía"
                num = (input("Introduce un número a eliminar: "))
                lista.remove(int(num))
            elif opcion == 3:
                posicion = (input("Introduce una posición a eliminar: "))
                lista.pop(int(posicion))

            print("Estado de la lista: ",lista)
            imprimir_opciones()
            opcion = int(input("Introduce una opción: "))

        except AssertionError as error:
            print("No se ha podido realizar la operación")
            print(error)
            imprimir_opciones()
            opcion = int(input("Introduce una opción: "))
        except:
            print("No se ha podido realizar la operación")
            imprimir_opciones()
            opcion = int(input("Introduce una opción: "))

    print("Adiós")

lista = []
menu2(lista)
