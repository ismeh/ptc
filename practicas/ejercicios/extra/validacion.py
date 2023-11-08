"""
Ejercicio validar entrada de euros.
Hay que realizar una función para leer un precio en euros que solo admita valores correctos.
"""

"""
Lee dígitos y el punto
La parte decimal tiene como máximo 2 decimales
"""

"Mientras que no introduzcamos un valor correcta el programa nos vuelve a pedir un número"
def leer_euros():
    valor_correcto = False
    entrada = ""
    while (valor_correcto != True):
        continuar = True  # Continuar haciendo comprobaciones (si acaba en True el valor es correcto)
        entrada = input("Introduce una cantidad de dinero: ")
        cadenas = entrada.split(".")

        #Compruebo si esta vacio con if (entrada)
        if entrada:
            # Comprobar que todo son números

            n_puntos = 0
            for letra in entrada:
                if not letra.isdigit():
                    if letra == '.':
                        n_puntos += 1
                    else:
                        continuar = False

            if n_puntos > 1:
                continuar = False

            # Comprobar si negativo
            if len(cadenas[0]) > 0:
                if cadenas[0][0] == '-':
                    continuar = False

            #Comprobar parte decimal (si tiene) -> (menos de 3 digitos)
            if len(cadenas) > 1:
                if len(cadenas[1]) > 2:
                    continuar = False



        #Finalizar / Repetir
        if(continuar == True):
            valor_correcto = True
        if(valor_correcto == False):
            print("Número incorrecto")

    return float(entrada)


dinero = leer_euros()
print(f"\nHas introducido la cantidad de {dinero} €")