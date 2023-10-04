"""
4. Realizar un programa para una caja de un supermercado que lea un precio desde el teclado y una
cantidad entregada por el cliente (se supone que cantidad >= precio) y obtenga en la pantalla el
numero mnimo de monedas de 1 euro, 50 centimos, 10 centimos y 1 centimo que se deben dar de
cambio. Por ejemplo, si precio es 1.12 euros y cantidad es 5 euros, debe dar como resultado 3
monedas de 1 euro, 1 moneda de 50 centimos, 3 monedas de 10 centimos y 8 monedas de 1
centimo.
"""
import math

def calcularCambioMoneda(dinero, centimos):
      cantidad_monedas, cambio_restante = divmod(dinero, centimos)
      return cambio_restante, cantidad_monedas

precio = float(input("Introduzca el precio: "))
cantidad = float(input("Introduzca el dinero entregado: "))

cambio_restante = cantidad - precio
cambio_restante = int(cambio_restante * 100) #Para no perder centimos con la precisión decimal de python

cambio_restante, m_euro = calcularCambioMoneda(cambio_restante, 100)
cambio_restante, m_cincuenta = calcularCambioMoneda(cambio_restante, 50)
cambio_restante, m_diez = calcularCambioMoneda(cambio_restante, 10)
cambio_restante, m_uno = calcularCambioMoneda(cambio_restante, 1)

print("Resultado: ", m_euro, "monedas de 1 euro,", m_cincuenta, "monedas de 50 cent.,",
      m_diez, "monedas de 10 cent.,", m_uno, "monedas de 1 cent.,")