"""
Comprobar si los parámetros de las funciones pasan por valor o
por referencia
    Paso por valor: Se copia el valor dentro de la función y el original no se modifica
    Paso por referencia: Pasas el puntero por lo que accedes directamente a memoria y el dato original cambia
Dado un parámetro ver si dentro de la función puedo modificar su valor
¿Que ocurre fuera de la función?
"""

def test_param(param1):
    param1 += 1
    return param1

entero = 3

print("Prueba con enteros")
print("Lo que devuelve la funcion " + str(test_param(entero)))
print("El entero tras llamar a la función " + str(entero))

print("\nPrueba con listas")
lista = [1,2,3,4]
print(lista)
print(id(lista))


def test_param2(param1):
    print(id(param1))
    param1.append(10)
    print(id(param1))
    param1 = [0]
    print(id(param1))


print(test_param2(lista))
print(lista)
print(id(lista))

#En python los parametros se pasan como copias de las direcciones de memoria

