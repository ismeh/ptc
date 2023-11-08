# -*- coding: utf-8 -*-
#Ejercicio


def leerFloatMax2Decimales(mensaje):
    """
    Vemos si es un digito numérico y formato 99.99.
    Sirve para euros e interés. Se queda pidiendo el dato hasta que esté
    correcto y devuelve el float positivo con dos decimales.
    Entrada: mensaje para pedir el dato concreto.
    Salida: valorValidado, numeroIntentosIncorrectos.
    """
    numeroIntentosIncorrectos = 0
    valorValidado = False

    while not valorValidado:
        try:
            # número con 2 digitas y 2 decimales
            valorIntroducido = input(mensaje)
            digito = float(valorIntroducido)
            assert len(valorIntroducido.split(".")[1]) <= 2, f"La entrada debe tener como mucho 2 decimales: {digito}"
            print(f"CORRECTO {digito}")
            valorValidado = True
        except ValueError:
            print(f"Debe introducir un número flotante, usted introdujo: {valorIntroducido}")
            numeroIntentosIncorrectos += 1
        except IndexError:
            print(f"CORRECTO {digito}")
            valorValidado = True
        except AssertionError as error:
            print(error)
            numeroIntentosIncorrectos += 1

    return digito, numeroIntentosIncorrectos

def leerEnteroPositvo(mensaje):
    """
    Vemos si es un digito numérico entero (sin decimales) y positivo.
    Se queda pidiendo el dato hasta que esté correcto y devuelve el
    entero positivo.
    Entrada: mensaje para pedir el dato concreto.
    Salida: valorValidado, numeroIntentosIncorrectos.
    """
    numeroIntentosIncorrectos=0
    valorValidado=False

    while not valorValidado:
        try:
            valorIntroducido = input(mensaje)
            digito = int(valorIntroducido)
            assert digito> 0, f"La entrada es positiva y ha indicado {digito}"
            print(f"CORRECTO {digito}")

            valorValidado=True
        except ValueError:
            print(f"Debe introducir un número entero, usted introdujo: {valorIntroducido}")
            numeroIntentosIncorrectos+=1
        except AssertionError as error:
            print(error)
            numeroIntentosIncorrectos+=1

    return digito, numeroIntentosIncorrectos



if __name__=="__main__":
    nombreEstudiante="Ismael Tengo Rodríguez"
    nCorrectas=0
    nIncorrectas=0
    capital, nInc=leerFloatMax2Decimales("Dime capital inicial con 2 decimales máximo: ")
    nCorrectas+=1
    nIncorrectas=nIncorrectas+nInc
    interés, nInc=leerFloatMax2Decimales("Dime interés anual con 2 decimales máximo: ")
    nCorrectas+=1
    nIncorrectas=nIncorrectas+nInc
    anios, nInc =leerEnteroPositvo("Dime el número de años: ")
    nCorrectas+=1
    nIncorrectas=nIncorrectas+nInc
    print("Fin del programa de validación de euros")
    print("Nombre estudiante: ",nombreEstudiante)
    print("Entradas correctas: ",nCorrectas," incorrectas: ",nIncorrectas)

#Solución 3 correctas y 8 incorrectas


