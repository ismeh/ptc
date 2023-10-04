"""
2. Dados tres números x1, x2, x3, calcular la desviación típica respecto a su media aritmética.
"""

import math

CANTIDAD_NUMEROS = 3

x1=float(input("Ingrese el primer numero: "))
x2=float(input("Ingrese el segundo numero: "))
x3=float(input("Ingrese el tercer numero: "))

media = (x1+x2+x3)/ CANTIDAD_NUMEROS

desviacion_tipica = math.sqrt(((x1 - media)**2 + (x2 - media)**2 + (x3 - media)**2) / CANTIDAD_NUMEROS)

print("Media: ", media)
print("La desviación típica de los 3 números es: ", round(desviacion_tipica, 3))