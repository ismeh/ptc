# -*- coding: utf-8 -*-
"""
R3. Usando Matplotlib, para las 10 comunidades con más población media de 2010 a 2017, generar un gráfico de columnas
    que indique la población de hombres y mujeres en el año 2017, salvar el gráfico a fichero e incorporarlo a la
    página web 2 del punto R2.

    Ficheros Datos
        poblacionProvinciasHM2010-17.csv
        comunidadAutonoma-Provincia.html
        comunidadesAutonomas.html

    Resultado
        poblacionComAutonomas.html
        R3.png
"""

import csv
import locale
import numpy
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt # Para la gráfica

import funciones as func

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
    dic_cod_com = lista_to_dict_con_espacios(lista_comunidades, (0, 1), 2) #Key(codigo comunidad) - Value(comunidad) Bien escrito
    dic_ca = lista_to_dict(lista_comunidades, (1, 0), 2) #Key(comunidad) - Value(codigo comunidad)
    dic_pro= lista_to_dict(lista_provincias, (2, 3), 4) #Key(codigo provincia) - Value(provincia)
    dic_ca_pro = lista_to_dict_vector(lista_provincias, (1, 2), 4) #Key Comunidad- Valor Vector(Codigo Prov)
    PROVINCIAS = (dic_pro.values())
    datos_poblacion_provincia = csv_poblacion_to_numpy(ruta_datos, len(PROVINCIAS), len(SECCIONES), anios)

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

    def media_poblacion_comunidad(diccionario_pob_com, inicio, fin) -> dict:
        """Calcula la media de población de cada comunidad autónoma

        Args:
            diccionario_pob_com: Diccionario con la población de cada comunidad autónoma por años
            inicio: Indice del Año inicial
            fin: Indice del Año final

        Returns:
            mPobTCom: Diccionario con la media de población de cada comunidad autónoma
        """
        mPobTCom = {}
        for comunidad in diccionario_pob_com:
            mPobTCom[comunidad] = np.mean(diccionario_pob_com[comunidad][inicio:fin])

        return mPobTCom
    mPobTCom = media_poblacion_comunidad(dic_pob_com, 0, 8) #Dic Media de población de cada comunidad autónoma entre 2017 y 2010
    """ Ordenar diccionario por valor
        -https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        -https://www.w3schools.com/python/ref_func_sorted.asp
    """
    mPobTCom_orden_desc = (sorted(mPobTCom.items(), key=lambda item: item[1], reverse=True)) # Lista con las comunides ordenadas de mayor a menor población

    com_orden_desc10MPobT = mPobTCom_orden_desc[:10] # Top 10 tuplas Comunidad-Poblacion
    com_orden_desc10MPobT = [tupla[0] for tupla in com_orden_desc10MPobT]  #Lista con las 10 comunidades con mayor población
    def grafica_barras(datos, orden_com, titulo, ruta, dic_cod_com, dic_ca):
        """Crea una gráfica de barras a partir de los datos

        Args:
            datos: Datos de la gráfica
                Diccionario con
        """
        comunidades_sin_cod = orden_com
        comunidades_con_cod = []

        #Solo el nombre bien escrito
        for com_rankin in orden_com:
            comunidades_con_cod.append(dic_cod_com[dic_ca[com_rankin]])

        # #Para añadir el código
        # for com_rankin in orden_com:
        #     comunidades_con_cod.append(dic_ca[com_rankin] + " " + dic_cod_com[dic_ca[com_rankin]])

        idx_H = 8
        idx_M = 16
        datosM2017 = []
        datosH2017 = []
        ejeX = np.arange(len(comunidades_con_cod))
        ancho_barras = 0.25
        etiquetas = ['Hombres', 'Mujeres']
        colores=  ['b', 'r']

        for comunidad in comunidades_sin_cod:
            datosM2017.append(datos[comunidad][idx_M])
            datosH2017.append(datos[comunidad][idx_H])

        datosY = [datosH2017, datosM2017]

        # plt.figure(figsize=(15, 15)) #No hace falta si al guardar uso bbox_inches='tight'
        for i in range(len(etiquetas)):
            plt.bar(ejeX + ancho_barras*i, datosY[i], color=colores[i], width=ancho_barras)

        plt.xticks(ejeX+ancho_barras/2, comunidades_con_cod)


        #Leyenda
        plt.legend(labels=etiquetas)

        plt.xticks(rotation=80)
        plt.title(titulo)
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()

    nombre_img = "R3.png"
    src_img = func.DIRECTORIO_IMAGENES + nombre_img
    grafica_barras(dic_pob_com, com_orden_desc10MPobT, "Población por sexo en el año 2017", src_img, dic_cod_com, dic_ca)
    ruta_img_respecto_html = "../" + src_img

    #html
    paginaWeb = func.inicioHTML("Web 2", func.RUTA_ESTILO + "estilo2.css")
    paginaWeb += cuerpoHTML(SECCIONES, atributos, dic_pob_com, lista_comunidades_original_sin_codigo, dic_ca) #Tabla
    paginaWeb += func.imagenHTML(ruta_img_respecto_html, "Error al cargar la imagen", dimensiones=(720,720)) #Imagen
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
def ejercicio3():
    # Configuración de formato de números en output
    locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

    # Constantes - Datos
    FICHERO_SALIDA = func.DIRECTORIO_RESULTADOS + "poblacionComAutonomas.html"

    lista_comunidades = leerHtml(func.FICHERO_DATOS_ca)
    lista_provincias = leerHtml(func.FICHERO_DATOS_cap)

    #Eliminar la fila de ""Ciudades autonomas"
    lista_provincias_parte1 = lista_provincias[:-11]
    lista_provincias_parte2 = lista_provincias[-8:]
    lista_provincias = lista_provincias_parte1 + lista_provincias_parte2

    func.prepararCSV(func.FICHERO_DATOS_pp, func.DATOS_LIMPIOS, "Total Nacional", "Notas", verbose=False)
    crearHtml(FICHERO_SALIDA, func.DATOS_LIMPIOS, lista_comunidades, lista_provincias)

if __name__ == "R3":  # Cada vez que lo importe se ejecutará lo que esté aquí dentro
    print("Importando/Ejecutando R3.py")
    ejercicio3()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    ejercicio3()


