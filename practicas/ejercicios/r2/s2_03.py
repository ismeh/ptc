"""
3. Realizar un programa que lea una cantidad de horas, minutos y segundos con valores arbitrarios,
y los transforme en una expresion de tiempo convencional en la que los minutos y segundos dentro
del rango [0,59]. Por ejemplo, dadas 10 horas, 119 minutos y 280 segundos, debera dar como
resultado 12 horas, 3 minutos y 40 segundos.
"""


horas=int(input("Ingrese las horas: "))
minutos=int(input("Ingrese los minutos: "))
segundos=int(input("Ingrese los segundos: "))

minutos = minutos + segundos // 60
segundos = segundos % 60

horas = horas + minutos // 60
minutos = minutos % 60

print("Los valores anteriores se han convertido en: ", horas , "horas, ", minutos, "minutos y ", segundos, "segundos")