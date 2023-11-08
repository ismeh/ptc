""" Segundo fichero de participacion"""

import financiacion

euros = financiacion.leerFloat2decimales()
interes = financiacion.leerFloat2decimales()
anios = financiacion.leerInt()

resultado = 0
for i in range(anios):
    resultado = financiacion.calcularCapitalAnual(euros, interes)
    euros = resultado
print("Resultado: ", resultado, "euros")