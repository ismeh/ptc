# -*- coding: utf-8 -*-
"""
R4. Generar una página web 3 (fichero variacionComAutonomas.html) con una tabla
con la variación de población por comunidades autónomas desde el año 2011 a 2017,
indicando variación absoluta, relativa y desagregando dicha información
por sexos, es decir, variación absoluta (hombres, mujeres) y relativa (hombres,
mujeres). Para los cálculos, hay que actuar de manera semejante que en el apartado R1.

    Ficheros Datos
        poblacionProvinciasHM2010-17.csv
        comunidadAutonoma-Provincia.html
        comunidadesAutonomas.html

    Resultado
        variacionComAutonomas.htm
"""

import csv
import locale
import numpy
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt # Para la gráfica

import funciones as func

def cuerpoHTML(SECCIONES, SUB_SECCIONES, SECCIONES_CSV, secciones_bajo_cabeceras, atributos, dic_variacion_comunidades, datos_com, lista_comunidades_original, dic_ca):
    """Crea el cuerpo del fichero HTML, es decir la tabla con los datos

    Returns:
        paginaPob: Cuerpo del fichero HTML
    """

    # Tabla
    paginaWeb = """<table>"""

    #Años
    num_secciones_bajo_cabecera = len(secciones_bajo_cabeceras)

    # Cabeceras de la tabla
    paginaWeb += """
            <tr>
            <th></th>
            <th colspan={0}>Variación Absoluta</th>
            <th colspan={0}>Variación Relativa</th>
            </tr>
        """.format((num_secciones_bajo_cabecera-1)*len(SUB_SECCIONES))
    paginaWeb += "<tr> <th></th>"
    for seccion in SECCIONES:
        paginaWeb += """
            <th colspan={0}>Hombres</th>
            <th colspan={0}>Mujeres</th>
        """.format(num_secciones_bajo_cabecera-1)
    paginaWeb += "</tr>"

    # for header in range(len(SECCIONES)):
    paginaWeb += "<tr> <th></th>"
    for headers in range(len(SECCIONES)*len(SUB_SECCIONES)):
        for atr in atributos[1:num_secciones_bajo_cabecera]:
            paginaWeb += "<th>%s</th>" % (atr[1:]) #Reemplazar la letra por un vacio
    paginaWeb += "</tr>"

    # Filas tabla
    columnas_procesar = (num_secciones_bajo_cabecera - 1)*len(SECCIONES)*len(SUB_SECCIONES)
    for n in range(len(dic_variacion_comunidades)):
        comunidad_sin_espacio = lista_comunidades_original[n].replace(" ", "")
        paginaWeb += "<tr><td>%s</td>" % (lista_comunidades_original[n]) #Comunidad sin codigo
        for i in range(0, columnas_procesar):  # Empezamos desde la col 2017
            # Al tranformar el dato con locale, usamos %s para string en lugar de %f para float
            if(i < columnas_procesar/2):
                paginaWeb += "<td>%s</td>" % locale.format_string('%.0f', dic_variacion_comunidades[comunidad_sin_espacio][i], grouping=True)
            else:
                paginaWeb += "<td>%s</td>" % locale.format_string('%.2f', dic_variacion_comunidades[comunidad_sin_espacio][i], grouping=True)
        paginaWeb += "</tr>"
    paginaWeb += "</table>"


    return paginaWeb

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
    SECCIONES = ["Variación absoluta", "Variación relativa"]
    SUB_SECCIONES = ["Hombre", "Mujer"]
    SECCIONES_CSV = ["T", "H", "M"]
    secciones_bajo_cabeceras = int((len(atributos)-1)/len(SECCIONES_CSV)) #años=8
    secciones_bajo_cabeceras = atributos[1:secciones_bajo_cabeceras+1] # T2017-T2010

    #Comunidades
    lista_comunidades_original_sin_codigo = lista_comunidades[1::2]
    dic_cod_com = lista_to_dict_con_espacios(lista_comunidades, (0, 1), 2) #Key(codigo comunidad) - Value(comunidad) Bien escrito
    dic_ca = lista_to_dict(lista_comunidades, (1, 0), 2) #Key(comunidad) - Value(codigo comunidad)
    dic_pro= lista_to_dict(lista_provincias, (2, 3), 4) #Key(codigo provincia) - Value(provincia)
    dic_ca_pro = lista_to_dict_vector(lista_provincias, (1, 2), 4) #Key Comunidad- Valor Vector(Codigo Prov)
    PROVINCIAS = (dic_pro.values())
    datos_poblacion_provincia = csv_poblacion_to_numpy(ruta_datos, len(PROVINCIAS), len(SECCIONES_CSV), len(secciones_bajo_cabeceras))

    def poblacion_comunidad(d_pob_prov, dic_ca, dic_ca_pro, dic_pro) -> dict:
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

        #Añado los valores a la estructura
        for d_provincia in d_pob_prov:
            codigo = codigo_to_str_x_digitos(d_provincia[0])
            provincia = dic_pro[codigo]
            com_actual = buscar_provincia_in_dict_comunidad(dic_ca_pro, codigo)
            dic_pob_com[com_actual] += d_provincia[1:]

        return dic_pob_com
    dic_pob_com = poblacion_comunidad(datos_poblacion_provincia, dic_ca, dic_ca_pro,dic_pro) #Datos de población de cada comunidad autónoma

    def variacion_comunidades(poblacion_comunidades, secciones_bajo_cabecera) -> dict:
        """Calcula la variación de población de las comunidades autónomas para hombres y mujeres entre 2010 y 2017

        Args:
            poblacion_comunidades: Diccionario con la población de cada comunidad autónoma
            secciones_bajo_cabecera: Años de los datos del csv de población (2010-2017)
        Returns:
            variacion_comunidades: Diccionario con la variación absoluta y relativa de población de cada comunidad autónoma
        """
        variacion_comunidades = {}
        columna_inicial = len(secciones_bajo_cabecera) #Para saltarnos el total
        for comunidad in poblacion_comunidades:
            var_abs = np.zeros((len(secciones_bajo_cabecera) - 1) * 2, dtype=numpy.float32)
            var_rel = np.zeros((len(secciones_bajo_cabecera) - 1) * 2, dtype=numpy.float32)

            def variacion(funcion, almacenamiento):
                for anio in range(0, len(secciones_bajo_cabecera)-1):
                    almacenamiento[anio] = funcion(poblacion_comunidades[comunidad][anio + columna_inicial],
                                                    poblacion_comunidades[comunidad][anio+1 + columna_inicial])
                    almacenamiento[anio + len(secciones_bajo_cabecera)-1] = funcion(
                                                    poblacion_comunidades[comunidad][anio + columna_inicial*2],
                                                    poblacion_comunidades[comunidad][anio + columna_inicial*2+1])
            variacion(func.variacion_absoluta, var_abs)
            variacion(func.variacion_relativa, var_rel)

            var_combinada = np.concatenate((var_abs, var_rel), axis=0)

            variacion_comunidades[comunidad] = var_combinada

        return variacion_comunidades
    dic_variacion_comunidades = variacion_comunidades(dic_pob_com, secciones_bajo_cabeceras)

    #html
    paginaWeb = func.inicioHTML("Web 3", func.RUTA_ESTILO + "estilo2.css")
    paginaWeb += cuerpoHTML(SECCIONES, SUB_SECCIONES, SECCIONES_CSV, secciones_bajo_cabeceras, atributos, dic_variacion_comunidades, dic_pob_com, lista_comunidades_original_sin_codigo, dic_ca) #Tabla
    paginaWeb += func.finHTML()

    f.write(paginaWeb)
    fichero_csv.close()
    f.close()
    print("Se ha guardado la web en ", destino)

def lista_to_dict_con_espacios(lista, key_value, num_atributos) -> dict:
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
        diccionario[str(clave).replace(" ", "")] = str(valor)

    return diccionario
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
def ejercicio4():
    # Configuración de formato de números en output
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

    # Constantes - Datos
    FICHERO_SALIDA = func.DIRECTORIO_RESULTADOS + "variacionComAutonomas.html"

    lista_comunidades = leerHtml(func.FICHERO_DATOS_ca)
    lista_provincias = leerHtml(func.FICHERO_DATOS_cap)

    #Eliminar la fila de ""Ciudades autonomas"
    lista_provincias_parte1 = lista_provincias[:-11]
    lista_provincias_parte2 = lista_provincias[-8:]
    lista_provincias = lista_provincias_parte1 + lista_provincias_parte2

    func.prepararCSV(func.FICHERO_DATOS_pp, func.DATOS_LIMPIOS, "Total Nacional", "Notas", verbose=False)
    crearHtml(FICHERO_SALIDA, func.DATOS_LIMPIOS, lista_comunidades, lista_provincias)

if __name__ == "R4":  # Cada vez que lo importe se ejecutará lo que esté aquí dentro
    print("Importando/Ejecutando R4.py")
    ejercicio4()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    ejercicio4()


