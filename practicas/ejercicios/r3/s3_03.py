"""
3. Escribe una función mayusculas_minusculas(palabra) que devuelva una cadena en la que las
mayúsculas y las minúsculas estén al contrario.
"""


def mayusculas_minusculas(palabra):
    DIFERENCIA_MAY_MIN = ord('z') - ord('Z')
    nueva_palabra = ""
    for letra in palabra:
        if letra > 'Z':
            nueva_palabra += chr(ord(letra) - DIFERENCIA_MAY_MIN)
        else:
            nueva_palabra += chr(ord(letra) + DIFERENCIA_MAY_MIN)

    return nueva_palabra
def mayusculas_minusculas2(palabra):
    return palabra.swapcase()

print("Palabra original: HoOlAo")
print(mayusculas_minusculas("HoOlAo"))
print(mayusculas_minusculas2("HoOlAo"))

