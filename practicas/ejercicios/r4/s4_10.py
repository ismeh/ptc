"""
    Relación 4: listas
        Realizar dos versiones de cada ejercicio (si es posible)
            1. Sin usar los métodos de list
            2. Usando los métodos de list
    
    10. Leer una frase de teclado e implementar una función que devuelva una lista de pares en la que
debe aparecer cada letra junto a su frecuencia de aparición. Los espacios no se deben tener en
cuenta. Dicha lista debe estar ordenada atendiendo al orden ascendente de las letras. Ejemplo: ante
la entrada “programa” debe dar como salida [('a', 2), ('g', 1), ('m',1), ('o', 1), ('p',1), ('r',2)].
"""
import random
RAND_INF = 1
RAND_SUP = 10
SEMILLA = 0
random.seed(SEMILLA)

def ordenar(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] > lista[j]:
                lista[i], lista[j] = lista[j], lista[i]
    return lista

#Entrada de datos
frase = (input("Introduce una frase: "))

#Función 1
def frecuencia_letras(frase):
    lista = []
    for letra in frase:
        if letra != " " and letra not in lista:
            lista.append(letra)
    ordenar(lista)
    lista2 = []
    for letra in lista:
        if (letra, lista.count(letra)):
            lista2.append((letra, frase.count(letra)))
    return lista2

#Función 2
def frecuencia_letras2(frase):
    lista = []
    for letra in frase:
        if letra != " " and letra not in lista:
            lista.append(letra)
    lista.sort()
    lista2 = [(letra, frase.count(letra)) for letra in lista]
    return lista2

#Salida de datos
print("Frase: ", frase)
print("Frecuencia de letras: ", frecuencia_letras(frase))
print("Frecuencia de letras: ", frecuencia_letras2(frase))