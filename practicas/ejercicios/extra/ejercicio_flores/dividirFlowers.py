# -*- coding: utf-8 -*-

import os
import glob
import shutil

idx_clase = 1
idx_img_actual = 0
num_img_por_clase = 80
lista_clases = []
dir_dataset = "dataset/"
fichero_clases = dir_dataset + "classes.txt"


#Directorio de trabajo
print("Directorio de trabajo es: ", os.getcwd())
print() #Directorios y ficheros

# Leer fichero de clases y crear directorios
with open(fichero_clases, "r") as f:
    for linea in f:
        linea_nueva = linea.split('\n')[0]
        lista_clases.append(linea_nueva)
        os.makedirs(linea_nueva, exist_ok=True) #Crea el directorio incluso si existe

# print(lista_clases)

#Por cada imagen del dataset la renombramos y la copiamos en su directorio
for img in sorted(glob.glob(dir_dataset + "*.jpg")):
    new_img_name = lista_clases[idx_clase-1] + "\\" + img.split('\\')[1] #
    new_img_name = new_img_name[:-4] + "_" + lista_clases[idx_clase-1] + "_" + str(idx_img_actual % (num_img_por_clase)+1) + ".jpg"
    # print(new_img_name)
    idx_img_actual += 1
    if idx_img_actual % (num_img_por_clase) == 0:
        idx_clase += 1
    shutil.copyfile(img, new_img_name)

