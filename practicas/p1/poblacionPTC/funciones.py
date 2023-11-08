# -*- coding: utf-8 -*-
"""
Fichero con las funciones generales a todos los ejercicios
También contiene algunas constantes comunes a todos los ejercicios
"""
DIRECTORIO_ENTRADAS = "entradas/"
DIRECTORIO_RESULTADOS = "resultados/"

# Funciones lambda para calcular variación absoluta y relativa
variacion_absoluta = lambda actual, anterior: actual - anterior
variacion_relativa = lambda actual, anterior: (variacion_absoluta(actual, anterior) / anterior) * 100
