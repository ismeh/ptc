#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 18:17:11 2021

@author: Eugenio

Correccion del ejercicio flowers
"""
import glob

dirDataset="dataset"
ficheroClases=dirDataset+"/classes.txt"

listaClases = [line.strip('\n') for line in open(ficheroClases,"r", encoding="utf8")]


#vemos la correccion cargando el fichero en una lista
imagesFichFlowers=list()

fichFlowers=open("flowerImages.txt", "r", encoding="utf8")

for linea in fichFlowers:
    imagesFichFlowers.append(linea.strip('\n'))

fichFlowers.close()

#Linux
listaImages=list()

for clase in listaClases:
    image_paths = sorted(glob.glob(clase+"/*.jpg"))
    for image in image_paths:
        listaImages.append(image)
'''        
#windows
listaImages=list()
for clase in listaClases:
    image_paths = sorted(glob.glob(clase+"/*.jpg"))
    for image in image_paths:
        listaImages.append(image.replace("\\", "/"))
'''

    

if (set(imagesFichFlowers)==set(listaImages)):
    print("Ejercicio correcto")
else:
    print("Ejercicio incorrecto")

