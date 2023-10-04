from math import sqrt

print("Introduce los catetos de un triangulo rectangulo")
print("Cateto 1: ", end="")
cateto1 = float(input())

print("Cateto 2: ", end="")
cateto2 = float(input())

hipotenusa = sqrt(cateto1**2 + cateto2**2)

print("La hipotenusa del triangulo con catetos", cateto1 ,"y", cateto2 ,"es", hipotenusa)
