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

def crearHtml(destino, ruta_datos):
    """Crea el fichero HTML con los datos de población (variación absoluta y relativa)

    Args:
        destino: Ruta del fichero de salida
        ruta_datos: Ruta del fichero de datos
    """

    f = open(destino, 'w', encoding="utf8")

    datos = open(ruta_datos,
                 encoding="utf8")  # Datos con las columnas con las que quiero trabajr, el resto = None (hombres y mujeres)
    poblacionDict = csv.DictReader(datos, delimiter=';')  # Lector
    primera_fila = poblacionDict.__next__()  # Primera fila de datos, para sacar los atributos
    atributos = [k for k in primera_fila.keys() if k != None]  # Las columnas sin nombre son = None, las descarto
    num_atributos = len(atributos)
    MAIN_HEADER = 3  # Total-Hombre-Mujer


    paginaPob = """
    <!DOCTYPE html><html>
    <head><title>Web 2</title>
    <link rel="stylesheet" href="../estilo2.css">
    <meta charset="utf8"></head>
    <body>
    """

    # Tabla
    paginaPob += """<table>"""

    # Cabecera de la tabla
    paginaPob += """<tr>
        <th></th>
        <th rowspan=2>CCAA</th>
        <th colspan={0}>Total</th>
        <th colspan={0}>Hombres</th>
        <th colspan={0}>Mujeres</th>
        </tr>
        <tr>
    """.format(num_atributos - 1)  # -1 para quitar el primer atributo

    for header in range(MAIN_HEADER):
        for atr in atributos[1:]:  # Años Variación absoluta, -1 para no añadir 2010
            paginaPob += "<th>%s</th>" % (atr.replace('T', ''))
    paginaPob += "</tr>"


    # Filas tabla
    # Primera fila
    columnas_procesar = (num_atributos)
    paginaPob += "<tr><td>%s</td>" % (primera_fila[atributos[0]])
    for j in range(MAIN_HEADER):
        for i in range(1, columnas_procesar):  # Empezamos desde la col 2017
            siguiente = i + 1
            if j == 0:
                paginaPob += "<td>%s</td>" % locale.currency(func.variacion_absoluta(float(primera_fila[atributos[i]]),
                                                                                     float(primera_fila[
                                                                                               atributos[siguiente]])),
                                                             symbol=False,
                                                             grouping=True)  # Al tranforma el dato con locale, usamos %s para string en lugar de %f para float
            else:
                paginaPob += "<td>%s</td>" % locale.currency(func.variacion_relativa(float(primera_fila[atributos[i]]),
                                                                                     float(primera_fila[
                                                                                               atributos[siguiente]])),
                                                             symbol=False, grouping=True)
    paginaPob += "</tr>"

    # Resto de filas
    for fila in poblacionDict:
        paginaPob += "<tr><td>%s</td>" % (fila[atributos[0]])
        for j in range(MAIN_HEADER):
            for i in range(1, columnas_procesar):  # Empezamos desde la col 2017
                siguiente = i + 1
                if j == 0:
                    paginaPob += "<td>%s</td>" % locale.currency(
                        func.variacion_absoluta(float(fila[atributos[i]]), float(fila[atributos[siguiente]])),
                        symbol=False,
                        grouping=True)  # Al tranforma el dato con locale, usamos %s para string en lugar de %f para float
                else:
                    paginaPob += "<td>%s</td>" % locale.currency(
                        func.variacion_relativa(float(fila[atributos[i]]), float(fila[atributos[siguiente]])),
                        symbol=False, grouping=True)
        paginaPob += "</tr>"
    paginaPob += "</table></body></html>"

    f.write(paginaPob)
    datos.close()
    f.close()
    print("Se ha guardado la web en ", destino)

def leerHtml(fichero):
    """
        Lee un fichero HTML y extrae los datos de las celdas
        Args:
            fichero: Ruta local del fichero
    """
    comunidadesFich = open(fichero, 'r', encoding="utf8")

    comString = comunidadesFich.read() #Todo el HTML

    print("\nFichero leido ")

    soup = BeautifulSoup(comString, 'html.parser')

    celdas = soup.find_all('td')

    print(celdas)
    #
    # lista = []
    #
    # for celda in celdas:
    #     lista.append(celda.get_text())
    #
    # print("\nLista con los valores extraidos de las celdas\n", lista)
    #
    # tree = html.fromstring(comString)
    #
    # celdas = tree.xpath('//td/text()')
    #
    # print("\nLas celdas son\n", celdas)
def ejercicio2():
    # Configuración de formato de números en output
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

    # Constantes
    FICHERO_DATOS_pp = func.DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"
    FICHERO_DATOS_ca = func.DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
    FICHERO_DATOS_cap = func.DIRECTORIO_ENTRADAS + "comunidadAutonoma-Provincia.htm"
    DATOS_LIMPIOS = func.DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv"
    FICHERO_SALIDA = func.DIRECTORIO_RESULTADOS + "poblacionComAutonomas.html"


    prepararCSV(FICHERO_DATOS_pp, DATOS_LIMPIOS, "Total Nacional", "Notas", verbose=False)
    crearHtml(FICHERO_SALIDA, DATOS_LIMPIOS)

if __name__ == "R1":  # Cada vez que lo importe se ejecutará todo lo que esté aquí dentro
    ejercicio2()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    # ejercicio2()
    #
    # # Pruebas
    # datos = open(func.DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv", encoding="utf8")
    # poblacionDict = csv.DictReader(datos, delimiter=';')
    # print(poblacionDict.__next__())
    # a = (poblacionDict.__next__())
    # atributos = [k for k in a.keys() if k != None]  # Las columnas sin nombre son = None, las descarto
    # print(atributos)

    FICHERO_DATOS_ca = func.DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
    leerHtml(FICHERO_DATOS_ca)

