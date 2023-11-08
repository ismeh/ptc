# -*- coding: utf-8 -*-
"""
R1. Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos y
    relativos generando la página web 1 (que debe llamarse variacionProvincias.html)
"""
import numpy as np

# Funciones lambda para calcular variación absoluta y relativa
variacion_absoluta = lambda actual, anterior: actual - anterior
variacion_relativa = lambda actual, anterior: (variacion_absoluta(actual, anterior) / anterior) * 100

print(variacion_relativa(50,100))
print(variacion_absoluta(100,10))
