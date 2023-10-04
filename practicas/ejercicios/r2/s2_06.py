"""
6. Pedir tres valores reales x1,x2,x3, obtener su máximo y su mínimo y mostrarlos por pantalla. (No
usar la funcion max y min de python).
"""

x1 = float(input("Real 1: "))
x2 = float(input("Real 2: "))
x3 = float(input("Real 3: "))

max = x1
min = x1

if (x2 >= max):
    max = x2
if (x3 >= max):
    max = x3

if (x2 < min):
    min = x2
if (x3 < min):
    min = x3

print("El mínimo es:", min)
print("El máximo es:", max)
