"""
7. Realizar un programa que pida el nombre de una persona, primer apellido, segundo apellido y
que muestre por pantalla como sería el nombre completo en una sola línea. También mostrar el
nombre completo pero al revés. Finalmente volver a descomponer el nombre completo en sus tres
componentes y mostrarlos por pantalla
"""

nombre = input("Nombre: ")
apellido1 = input("Primer apellido: ")
apellido2 = input("Segundo apellido: ")

nombre_completo = nombre + " " + apellido1 + " " + apellido2
nombre_completo_invertido = nombre_completo[::-1]

descomposicion = nombre_completo.split(" ")

print("\nNombre completo:", nombre_completo)
print("Nombre completo al revés:", nombre_completo_invertido)

print("\nNombre separado:", descomposicion[0])
print("Primer apellido separado:", descomposicion[1])
print("Segundo apellido separado:", descomposicion[2])
