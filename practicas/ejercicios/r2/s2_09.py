"""
9. Realizar un programa que tomando como entrada la radiación solar media por día en Kwh/m2
calcule el número mínimo de paneles solares que se necesitan para producir, al menos, 1000 Kwh
en un mes (30 días) teniendo en cuenta que los paneles solares tienen un 17% de rendimiento y que
son de un tamaño de 1.6 m2
"""
import math

radiacion_solar = float(input("Radiación solar media por dia Kwh/m2: "))
PRODUCCION_MINIMA = 1000 # Kwh
DIAS_PRODUCCION = 30
RENDIMIENTO_PANELES = 0.17 # %
TAM_PANELES = 1.6 # m2

paneles_minimos = math.ceil(PRODUCCION_MINIMA / (DIAS_PRODUCCION * RENDIMIENTO_PANELES * TAM_PANELES * radiacion_solar))

print("Los paneles mínimos para que conseguir una producción de", PRODUCCION_MINIMA, "Kwh en un periodo de",
      DIAS_PRODUCCION, "días con unos paneles de", TAM_PANELES, "m2 y un rendimiento del", RENDIMIENTO_PANELES*100,
      "% es de", paneles_minimos, "paneles")