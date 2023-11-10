"""
R2. Usando el listado de comunidades autónomas que podemos obtener del fichero
    comunidadesAutonomas.html, así como de las provincias de cada comunidad autónoma que podemos obtener de
    comunidadAutonoma-Provincia.html y los datos de poblacionProvinciasHM2010-17.csv, hay que generar una página web 2
    (fichero poblacionComAutonomas.html) con una tabla con los valores de población de cada comunidad autónoma en cada
    año de 2010 a 2017, indicando también los valores desagregados por sexos (de manera semejante a como aparece en la
    siguiente figura). Las celdas deben tener el contenido centrado.

    Ficheros Datos
        poblacionProvinciasHM2010-17.csv
        comunidadAutonoma-Provincia.html
        comunidadesAutonomas.html

    Resultado
        poblacionComAutonomas.html
"""

import csv
import locale
import funciones as func
from bs4 import BeautifulSoup
from lxml import html



def prepararCSV(fichero, destino, palabra_inicial, palabra_final, verbose=False):
    """Modifica un fichero csv para que solo contenga los datos relevantes de población de las provincias españolas

    Args:
        fichero: Ruta del fichero
        destino: Ruta del fichero de salida
        palabra_inicial: Palabra que indica el inicio de los datos
        palabra_final: Palabra que indica el final de los datos
        verbose: Detalles del texto filtrado. Defaults to False.
    """
    archivo = open(fichero, "r", encoding="utf8")
    texto_archivo = archivo.read()

    if verbose:
        print("\nTexto leido: \n", texto_archivo)

    primero = texto_archivo.find(palabra_inicial)
    ultimo = texto_archivo.find(palabra_final)
    texto_final = texto_archivo[primero:ultimo]

    if verbose:
        print("\nTexto filtrado: \n", texto_final)

    cabecera = "Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010"
    fichero_final = open(destino, "w", encoding="utf8")
    fichero_final.write(cabecera + '\n' + texto_final)
    fichero_final.close()

    archivo.close()

def inicioHTML(nombre, estilo):
    """Crea el inicio del fichero HTML

    Args:
        nombre: Nombre de la web
        estilo: Ruta del fichero CSS

    Returns:
        inicio: Inicio del fichero HTML
    """

    inicio = """
    <!DOCTYPE html><html>
    <head><title>%s</title>
    <link rel="stylesheet" href=%s>
    <meta charset="utf8"></head>
    <body>
    """ % (nombre, estilo)

    return inicio

def cuerpoHTML(MAIN_HEADER, atributos, primera_fila, poblacionDict):
    """Crea el cuerpo del fichero HTML, es decir la tabla con los datos

    Returns:
        paginaPob: Cuerpo del fichero HTML
    """

    # Tabla
    paginaWeb = """<table>"""

    # Cabecera de la tabla
    paginaWeb += """<tr>
            <th rowspan=2>CCAA</th>
            <th colspan={0}>Total</th>
            <th colspan={0}>Hombres</th>
            <th colspan={0}>Mujeres</th>
            </tr>
            <tr>
        """.format((len(atributos) - 1)/len(MAIN_HEADER))  # -1 para quitar el primer atributo

    # for header in range(len(MAIN_HEADER)):
    for atr in atributos[1:]:  # Años Variación absoluta, -1 para no añadir 2010
        paginaWeb += "<th>%s</th>" % (atr[1:]) #Reemplazar la letra por un vacio
    paginaWeb += "</tr>"

    # Filas tabla
    # Primera fila IGNORAMOS TOTAL NACIONAL
    columnas_procesar = (len(atributos))

    # Resto de filas
    for fila in poblacionDict:
        paginaWeb += "<tr><td>%s</td>" % (fila[atributos[0]])
        for j in range(len(MAIN_HEADER)):
            for i in range(1, columnas_procesar):  # Empezamos desde la col 2017
                siguiente = i #cambiar esto
                if j == 0:
                    paginaWeb += "<td>%s</td>" % locale.currency(
                        func.variacion_absoluta(float(fila[atributos[i]]), float(fila[atributos[siguiente]])),
                        symbol=False,
                        grouping=True)  # Al tranforma el dato con locale, usamos %s para string en lugar de %f para float
                else:
                    paginaWeb += "<td>%s</td>" % locale.currency(
                        func.variacion_relativa(float(fila[atributos[i]]), float(fila[atributos[siguiente]])),
                        symbol=False, grouping=True)
        paginaWeb += "</tr>"
    paginaWeb += "</table>"


    return paginaWeb

def finHTML():
    """Crea el final del fichero HTML

    Returns:
        fin: Final del fichero HTML
    """

    fin = """</body></html>"""

    return fin
def crearHtml(destino, ruta_datos, lista_comunidades, lista_provincias):
    """Crea el fichero HTML con los datos de población (variación absoluta y relativa)

    Args:
        destino: Ruta del fichero de salida
        ruta_datos: Ruta del fichero de datos
    """

    f = open(destino, 'w', encoding="utf8")

    #Datos-Atributos-Cabeceras...
    #CSV
    fichero_csv = open(ruta_datos,
                 encoding="utf8")  # Datos con las columnas con las que quiero trabajr, el resto = None (hombres y mujeres)
    poblacionDict = csv.DictReader(fichero_csv, delimiter=';')  # Lector
    primera_fila = poblacionDict.__next__()  # Primera fila de datos, para sacar los atributos
    atributos = [k for k in primera_fila.keys() if k != None]  # Las columnas sin nombre son = None, las descarto
    MAIN_HEADER = ["Total", "Hombre", "Mujer"]
    #Comunidades
    dic_ca = lista_to_dict(lista_comunidades, (0, 1), 2)
    print(dic_ca)

    #html
    paginaWeb = inicioHTML("Web 2", "../estilo2.css")
    paginaWeb += cuerpoHTML(MAIN_HEADER, atributos, primera_fila, poblacionDict)
    paginaWeb += finHTML()



    f.write(paginaWeb)
    fichero_csv.close()
    f.close()
    print("Se ha guardado la web en ", destino)

def lista_to_dict(lista, key_value, num_atributos):
    """Convierte una lista en un diccionario

    Args:
        lista: Lista a convertir
        key_value: Tupla de atributos a usar como clave y valor
        num_atributos: Número de atributos de la lista

    Returns:
        diccionario: Diccionario con los datos de la lista
    """
    diccionario = {}
    for i in range(0, len(lista), num_atributos):
        diccionario[lista[i + key_value[0]]] = lista[i + key_value[1] - 1]

    return diccionario
def leerHtml(fichero):
    """
        Lee un fichero HTML y extrae los datos de las celdas
        Args:
            fichero: Ruta local del fichero
        Returns:
            lista: Lista con los valores extraidos de las celdas
    """
    comunidadesFich = open(fichero, 'r', encoding="utf8")

    comString = comunidadesFich.read() #Todo el HTML

    soup = BeautifulSoup(comString, 'html.parser')

    celdas = soup.find_all('td') #Todos los datos de las celdas HTML


    lista = []

    #Lista con los valores extraidos de las celdas
    for celda in celdas:
        lista.append(celda.get_text())

    # Otra opción para extraer los datos de las celdas (como en 'lista')
    # tree = html.fromstring(comString)
    # celdas = tree.xpath('//td/text()')

    return lista

def ejercicio2():
    # Configuración de formato de números en output
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

    # Constantes - Datos
    FICHERO_DATOS_pp = func.DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"
    FICHERO_DATOS_ca = func.DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
    FICHERO_DATOS_cap = func.DIRECTORIO_ENTRADAS + "comunidadAutonoma-Provincia.htm"
    DATOS_LIMPIOS = func.DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv"
    FICHERO_SALIDA = func.DIRECTORIO_RESULTADOS + "poblacionComAutonomas.html"

    lista_comunidades = leerHtml(FICHERO_DATOS_ca)
    lista_provincias = leerHtml(FICHERO_DATOS_cap)

    prepararCSV(FICHERO_DATOS_pp, DATOS_LIMPIOS, "Total Nacional", "Notas", verbose=False)
    crearHtml(FICHERO_SALIDA, DATOS_LIMPIOS, lista_comunidades, lista_provincias)

if __name__ == "R1":  # Cada vez que lo importe se ejecutará todo lo que esté aquí dentro
    ejercicio2()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    ejercicio2()
    # FICHERO_DATOS_ca = func.DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
    # # Pruebas
    # datos = open(func.DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv", encoding="utf8")
    # poblacionDict = csv.DictReader(datos, delimiter=';')
    # print(poblacionDict.__next__())
    # a = (poblacionDict.__next__())
    # atributos = [k for k in a.keys() if k != None]  # Las columnas sin nombre son = None, las descarto
    # print(atributos)


