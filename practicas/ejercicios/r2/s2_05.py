"""
5. Hacer un programa para calcular la diferencia en horas:minutos:segundos entre dos instantes de
tiempo dados en horas:minutos:segundos.
"""

entrada_datos = input("Introduce el primer tiempo HH:MM:SS\n")
tiempo = entrada_datos.split(":")
h1 = int(tiempo[0])
m1 = int(tiempo[1])
s1 = int(tiempo[2])

entrada_datos = input("Introduce el segundo tiempo HH:MM:SS\n")
tiempo = entrada_datos.split(":")
h2 = int(tiempo[0])
m2 = int(tiempo[1])
s2 = int(tiempo[2])

dif_h = abs(h1 - h2)
dif_m = abs(m1 - m2)
dif_s = abs(s1 - s2)

print("La diferencia entre los dos intervalos es de ", dif_h, "horas", dif_m, "minutos", dif_s, "segundos")