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

import numpy
import numpy as np

import funciones as func
from bs4 import BeautifulSoup

def prepararCSV(fichero, destino, palabra_inicial, palabra_final, verbose=False):
    """Modifica un fichero csv para que solo contenga los datos relevantes de población de las provincias españolas

    Args:
        fichero: Ruta del fichero
        destino: Ruta del fichero de salida
        palabra_inicial: Palabra que indica el inicio de los datos
        palabra_final: Palabra que indica el final de los datos
        verbose: Detalles del texto filtrado. Defaults to False.
    """
    cabecera = "Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011;H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010"
    archivo = open(fichero, "r", encoding="utf8")
    texto_archivo = archivo.read()

    if verbose:
        print("\nTexto leido: \n", texto_archivo)

    primero = texto_archivo.find(palabra_inicial)
    ultimo = texto_archivo.find(palabra_final)
    texto_final = texto_archivo[primero:ultimo]
    texto_escrito = cabecera + '\n' + texto_final

    if verbose:
        print("\nTexto escrito: \n", texto_escrito)

    fichero_final = open(destino, "w", encoding="utf8")
    fichero_final.write(texto_escrito)
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

def cuerpoHTML(SECCIONES, atributos, datos_com, lista_comunidades_original, dic_ca):
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
        """.format((len(atributos) - 1)/len(SECCIONES))  # -1 para quitar el primer atributo

    # for header in range(len(SECCIONES)):
    for atr in atributos[1:]:  # Años Variación absoluta, -1 para no añadir 2010
        paginaWeb += "<th>%s</th>" % (atr[1:]) #Reemplazar la letra por un vacio
    paginaWeb += "</tr>"

    # Filas tabla
    # Primera fila IGNORAMOS TOTAL NACIONAL
    columnas_procesar = (len(atributos)) - 1#Ignoramos primera columna
    # Resto de filas
    for n in range(len(datos_com)):
        comunidad_sin_espacio = lista_comunidades_original[n].replace(" ", "")
        paginaWeb += "<tr><td>%s</td>" % (dic_ca[comunidad_sin_espacio] + " " + lista_comunidades_original[n])
        for i in range(0, columnas_procesar):  # Empezamos desde la col 2017
            # Al tranformar el dato con locale, usamos %s para string en lugar de %f para float
            paginaWeb += "<td>%s</td>" % locale.format_string('%.0f', datos_com[comunidad_sin_espacio][i], grouping=True)
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
    SECCIONES = ["Total", "Hombre", "Mujer"]
    anios = 8 #2017-2010

    #Comunidades
    lista_comunidades_original_sin_codigo = lista_comunidades[1::2]
    dic_ca = lista_to_dict(lista_comunidades, (1, 0), 2) #Key(comunidad) - Value(codigo comunidad)
    dic_pro= lista_to_dict(lista_provincias, (2, 3), 4) #Key(codigo provincia) - Value(provincia)
    dic_ca_pro = lista_to_dict_vector(lista_provincias, (1, 2), 4) #Key Comunidad- Valor Vector(Codigo Prov)
    PROVINCIAS = (dic_pro.values())
    datos_poblacion_provincia = csv_poblacion_to_numpy(ruta_datos, len(PROVINCIAS), len(SECCIONES), anios)

    def poblacion_comunidad(d_pob_prov, dic_ca, dic_ca_pro, dic_pro):
        """Calcula la población de cada comunidad autónoma

        Args:
            d_pob_prov: Array de numpy con los datos de población
            dic_ca: Diccionario con las comunidades autónomas
            dic_capro: Diccionario con las provincias de cada comunidad autónoma
            dic_pro: Diccionario con las provincias

        Returns:
            d_pob_com: Diccionario con la población de cada comunidad autónoma por años
        """

        def codigo_to_str_x_digitos(codigo, digitos=2):
            """Convierte un código a string con x dígitos

            Args:
                codigo: Código a convertir
                digitos: Número de dígitos del código

            Returns:
                codigo_str: Código convertido a string
            """
            codigo_str = str(codigo)
            while len(codigo_str) < digitos:
                codigo_str = "0" + codigo_str

            return codigo_str
        def buscar_provincia_in_dict_comunidad(dic_comunidades_prov, cod_provincia):
                """Busca la provincia en el diccionario de comunidades autónomas

                Args:
                    dic_comunidades_prov: Diccionario de comunidades autónomas
                    cod_provincia: Código de la provincia a buscar

                Returns:
                    com_actual: Comunidad autónoma a la que pertenece la provincia
                """
                for comunidad in dic_comunidades_prov:
                    if cod_provincia in dic_comunidades_prov[comunidad]:
                        return comunidad

        #Creo la estructura del diccionario
        dic_pob_com = {}
        for comunidad in dic_ca:
            dic_pob_com[comunidad] = np.zeros(len(d_pob_prov[0])-1, dtype=numpy.int_) #Array de tantos datos como columnas en una fila(provincia) de los datos

        # print("d_pob_prov-1", len(d_pob_prov)-1)
        # print("d_provincia=d_pob_prov[0]-1", len(d_pob_prov[0])-1)
        # print("npArray", np.shape(d_pob_prov))
        # print("npArray fila datos", np.shape(d_pob_prov[0][1:]))
        # print("dic_pob_com", len(dic_pob_com.values()))
        # print("dic_pob_com[andalucia]", len(dic_pob_com["Andalucía"]))

        #Añado los valores a la estructura
        for d_provincia in d_pob_prov:
            codigo = codigo_to_str_x_digitos(d_provincia[0])
            provincia = dic_pro[codigo]
            com_actual = buscar_provincia_in_dict_comunidad(dic_ca_pro, codigo)
            dic_pob_com[com_actual] += d_provincia[1:]

        return dic_pob_com
    dic_pob_com = poblacion_comunidad(datos_poblacion_provincia, dic_ca, dic_ca_pro,dic_pro)
    print(dic_pob_com["Andalucía"])

    #html
    paginaWeb = inicioHTML("Web 2", "../estilo2.css")
    paginaWeb += cuerpoHTML(SECCIONES, atributos, dic_pob_com, lista_comunidades_original_sin_codigo, dic_ca)
    paginaWeb += finHTML()

    f.write(paginaWeb)
    fichero_csv.close()
    f.close()
    print("Se ha guardado la web en ", destino)

def lista_to_dict(lista, key_value, num_atributos) -> dict:
    """Convierte una lista en un diccionario
    Guardo tanto la key como los values como string sin espacio

    Args:
        lista: Lista a convertir
        key_value: Indices de los atributos de la lista a usar como clave y valor en el diccionario
        num_atributos: Número de atributos de la lista

    Returns:
        diccionario: Diccionario con los datos de la lista
    """
    diccionario = {}
    for i in range(0, len(lista), num_atributos):
        clave = lista[i + key_value[0]]
        valor = lista[i + key_value[1]]
        diccionario[str(clave).replace(" ", "")] = str(valor).replace(" ", "")

    return diccionario

def lista_to_dict_vector(lista, key_value, num_atributos) -> dict:
    """Convierte una lista en un diccionario
        Guardo tanto la key como los values como string sin espacio

    Args:
        lista: Lista a convertir
        key_value: Indices de los atributos de la 'lista' a usar como clave y valor(array) en el diccionario
        num_atributos: Número de atributos de la lista

    Returns:
        diccionario: Diccionario con clave-tupla
    """
    diccionario = {}
    for i in range(0, len(lista), num_atributos):
        valor = lista[i + key_value[1]]
        valor = str(valor).replace(" ", "")
        clave = lista[i + key_value[0]]
        clave = str(clave).replace(" ", "")

        #Si comunidad existe en diccionario, añadir provincia, sino crear comunidad y añadir provincia
        if clave in diccionario:
            diccionario[clave].append(valor)
        else:
            diccionario[clave] = [valor]

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

def csv_poblacion_to_numpy(ruta_csv_filtrado, filas, num_secciones, num_atributos) -> np.ndarray:
    """Convierte un fichero CSV a un array de numpy

    Args:
        csv_filtrado: Ruta del fichero CSV con los datos de población
        filas: Número de filas del fichero
        secciones: Número de veces que se repiten los atributos (T-H-M)
        atributos: Número de atributos del fichero (Cada año 2017-2010)

    Returns:
        poblacion: Array de numpy con los datos del fichero
            La primera columna es el código de provincia, el resto son los datos de población
    """
    fichero_csv = open(ruta_csv_filtrado,
                       encoding="utf8")  # Datos con las columnas con las que quiero trabajr, el resto = None (hombres y mujeres)
    lectorLista = csv.reader(fichero_csv, delimiter=';') #Lectura del csv como list
    columnas = num_secciones * num_atributos + 1 #+1 para la columna del codigo de provincia
    poblacion_np = np.zeros((filas, columnas), dtype=numpy.int_)

    #Ignoro las dos primeras filas (Cabecera y Total Nacional)
    lectorLista.__next__(); lectorLista.__next__();

    for i in range(filas):
        f_datos = lectorLista.__next__()

        #Extraigo el código de la provincia
        codigo_provincia = str(f_datos[0]).split(" ")[0] #Casteo para autocompletado (se puede quitar)

        #Sustituyo el código de la provincia por el nombre de la provincia - Problema aparece como 2 en lugar de 02
        f_datos[0] = int(codigo_provincia)

        #Añado los datos de población al np.ndarray #Lo añado 1 a 1 porque tengo que castear los valores
        for j in range(columnas):
            poblacion_np[i][j] = float(f_datos[j])

    fichero_csv.close()
    return poblacion_np
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

    #Eliminar la fila de ""Ciudades autonomas"
    lista_provincias_parte1 = lista_provincias[:-11]
    lista_provincias_parte2 = lista_provincias[-8:]
    lista_provincias = lista_provincias_parte1 + lista_provincias_parte2

    prepararCSV(FICHERO_DATOS_pp, DATOS_LIMPIOS, "Total Nacional", "Notas", verbose=False)
    crearHtml(FICHERO_SALIDA, DATOS_LIMPIOS, lista_comunidades, lista_provincias)

if __name__ == "R1":  # Cada vez que lo importe se ejecutará todo lo que esté aquí dentro
    ejercicio2()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    ejercicio2()
    # FICHERO_DATOS_ca = func.DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
    # # Pruebas
    datos = open(func.DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv", encoding="utf8")
    # poblacionDict = csv.DictReader(datos, delimiter=';') #Lectura as dict
    # print(poblacionDict.__next__()["Provincia"])
    poblacionList = csv.reader(datos, delimiter=';') #Lectura as list
    # print(poblacionList.__next__()[1:9])
    # for reg in poblacionList:
    #     a = reg
    #     # print(reg)
    #     a[0] = a[0].split(" ")[0]
    #     print(a)

    # a = (poblacionDict.__next__())
    # atributos = [k for k in a.keys() if k != None]  # Las columnas sin nombre son = None, las descarto
    # print(atributos)

    # SECCIONES = 3
    # PROVINCIAS = 52
    # ATRIBUTOS = 8 #2017-2010
    # array_poblacion = csv_poblacion_to_numpy(datos, PROVINCIAS, SECCIONES, ATRIBUTOS)
    # print(array_poblacion)


