import math

print("Introduce el radio de la circunferencia")
radio = float(input())

longitud = 2 * math.pi * radio
area = math.pi * radio ** 2

print("La longitud del circulo con radio", radio ,"es", round(longitud,2) ,"y su area es" , round(area,2))
print("Longitud: ", round(longitud,3) ,"\tArea:" , round(area,3))
print("Radio:", radio ,"\t Longitud: ", round(longitud,2) ,"\tArea: " , round(area))

print(f"La longitud del círculo con radio {radio} es {round(longitud, 2)} y su área es {round(area, 2)}")
print("La longitud del círculo con radio %s es %.2f y su área es %.2f" % (radio, longitud, area))
print("La longitud del círculo con radio {} es {:.2f} y su área es {:.2f}".format(radio, longitud, area))