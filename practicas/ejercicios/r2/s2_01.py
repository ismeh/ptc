"""
1. Calcular precio de un vehículo suponiendo que tenemos que pedir como datos de entrada los
siguientes: precio bruto del vehículo, porcentaje de ganancia del vendedor, IVA a aplicar. El precio
base se calcula incrementando el precio bruto con el porcentaje de ganancia. El precio final será el
precio base incrementado con el porcentaje de IVA.
"""

precio_bruto = float(input("Introduzca el precio bruto del vehículo\n"))
porcentaje_ganancia = float(input("Introduzca el porcentaje de ganancia del vendedor\n"))
iva = float(input("Introduzca el IVA a aplicar\n"))

precio_base = precio_bruto * (1+porcentaje_ganancia/100)
precio_final = precio_base * (1+iva/100)

print("El precio final del vehículo es: ", round(precio_final, 3))