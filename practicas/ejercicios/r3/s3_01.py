"""
1. Escribe una función contar_letras(palabra, letra) que devuelva el número de veces que aparece una letra en una palabra.
"""

def contar_letras(palabra, letra):
    ocurrencias = 0
    for caracter in palabra:
        if caracter==letra:
            ocurrencias+=1
    return ocurrencias

def contar_letras2(palabra, letra):
    return palabra.count(letra)

print(contar_letras("hoolao", 'o'))
print(contar_letras2("hoolao", 'o'))
