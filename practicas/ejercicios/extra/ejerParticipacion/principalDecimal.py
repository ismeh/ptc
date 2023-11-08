"""Tercer programa

Igual que el segundo pero usando la librería decimal
"""

import financiacion
import decimal
from decimal import Decimal, getcontext

getcontext().rounding = decimal.ROUND_HALF_UP

euros = Decimal(financiacion.leerFloat2decimales())
interes = Decimal(financiacion.leerFloat2decimales())
anios = financiacion.leerInt()

def nuevoCalcularCapitalAnual(capitalInicial, interes):
    resultado = capitalInicial * (1 + interes / 100)
    return resultado.quantize(Decimal("1.00"))

resultado = 0
for i in range(anios):
    resultado = nuevoCalcularCapitalAnual(euros, interes)
    euros = resultado
print("Resultado: ", resultado, "euros")