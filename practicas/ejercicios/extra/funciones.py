# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:26:42 2019

@author: Eugenio
Ejemplo para crear módulos y diferenciar cuando se importa o no
"""

def funcion1():
    print("Módulo funciones. Función 1.")


def funcion2():
    print("Módulo funciones. Función 2.")
    

print("Se ejecuta siempre")
    
if __name__=="__main__":
    print("Módulo funciones es llamado como fichero principal")
    funcion1()
    funcion2()


if __name__=="funciones":
    print("Módulo funciones está siendo importado")
    

