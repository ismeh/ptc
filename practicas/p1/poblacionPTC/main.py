# -*- coding: utf-8 -*-
import os
import funciones as func

#Llamar al fichero R1.py
import R1 as r1
import R2 as r2
import R3 as r3
import R4 as r4
import R5 as r5

# Borrar fichero temporal
print("\nBorrando ficheros temporal")
os.remove(func.DATOS_LIMPIOS)

print("Se han ejecutado todos los archivos")

