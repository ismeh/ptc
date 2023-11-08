"""
Ejercicio 1
"""


""" Se queda pidiendo el dato hasta que esté correcto y devuelve el float con dos decimales"""
def leerFloat2decimales():
    valor_correcto = False
    entrada = ""
    while (valor_correcto != True):
        continuar = True  # Continuar haciendo comprobaciones (si acaba en True el valor es correcto)
        entrada = input("Introduce un numero: ")
        cadenas = entrada.split(".")

        # Compruebo si esta vacio con if (entrada)
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

            # Comprobar parte decimal (si tiene) -> (menos de 3 digitos)
            if len(cadenas) > 1:
                if len(cadenas[1]) > 2:
                    continuar = False

        # Finalizar / Repetir
        if (continuar == True):
            valor_correcto = True
        if (valor_correcto == False):
            print("Número incorrecto")

    return float(entrada)


"""Se queda pidiendo el dato hasta que esté correcto y devuelve el entero"""
def leerInt():
    valor_correcto = False
    entrada = ""
    while (valor_correcto != True):
        continuar = True  # Continuar haciendo comprobaciones (si acaba en True el valor es correcto)
        entrada = input("Introduce un numero: ")

        # Compruebo si esta vacio con if (entrada)
        if entrada:
            # Comprobar que todo son números
            for letra in entrada:
                if not letra.isdigit():
                    continuar = False

            # Comprobar si negativo
            if entrada[0] == '-':
                continuar = False

        # Finalizar / Repetir
        if (continuar == True):
            valor_correcto = True
        if (valor_correcto == False):
            print("Número incorrecto")

    return int(entrada)


"""
entrada: un float y la cantidad de decimales a redondear (usaremos 2)
salida: un float redondeado hacia arriba a partir de 0.5 (como en el caso de los euros)
"""
def redondear(numero, decimales=2):
    numero = numero * (10 ** decimales)
    numero = numero + 0.5
    numero = int(numero)
    numero = numero / (10 ** decimales)
    return numero

"""
entrada: un float en euros, con dos decimales, y un interés en tanto por cien con dos decimales
salida: suma de capital inicial + interes obtenido
es decir capitalAnual=capitalInicial+capitalInicial*interes/100.
la salida tiene que estar redondeada a 2 decimales pues estamos trabajando en euros
"""
def calcularCapitalAnual(capitalInicial, interes):
    return redondear(capitalInicial * (1 + interes / 100), 2)


if __name__ == "__main__":
    print(leerInt())
    print(leerFloat2decimales())
    print(redondear(0.34878))
    print(calcularCapitalAnual(543437.21, 1.34))

if __name__ == "financiacion":
    print("Módulo financiación está siendo importado")



