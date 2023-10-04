"""
8. Realizar un programa que pida un valor X de porcentaje de alcohol de una marca de cerveza y
que según dicho porcentaje calcule cuantos tercios de esa marca de cerveza (333cc) puedo tomar si
no quiero ingerir más de 50 cc de alcohol. Dar el resultado en valor entero.
"""
import math

alcohol = int(input("Introduzca porcentaje de alcohol: ")) / 100
VOLUMEN_TERCIO = 333
MAX_ALCOHOL_SANGRE = 50

num_cervezas_maximas = math.floor(MAX_ALCOHOL_SANGRE / (VOLUMEN_TERCIO * alcohol))

#print("cc de alcohol por cerveza: ", VOLUMEN_TERCIO * alcohol)
print("No puedo tomar más de ", num_cervezas_maximas, "cervezas de la marca ####")
