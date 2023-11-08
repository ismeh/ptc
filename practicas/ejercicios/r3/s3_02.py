"""
2. Escribe una función eliminar_letras(palabra, letra) que devuelva una versión de palabra que no
contiene el carácter letra ninguna vez
"""

def eliminar_letras(palabra, letra):
    nueva_palabra = ""
    for caracter in palabra:
       if caracter!=letra:
            nueva_palabra += caracter
    return nueva_palabra

def eliminar_letras2(palabra, letra):
    return palabra.replace('o','')

print(eliminar_letras("hoolao", 'o'))
print(eliminar_letras2("hoolao", 'o'))

