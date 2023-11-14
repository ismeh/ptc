# -*- coding: utf-8 -*-
"""
Fichero con las funciones generales a todos los ejercicios
También contiene algunas constantes comunes a todos los ejercicios
"""

#Constantes
DIRECTORIO_ENTRADAS = "entradas/"
DIRECTORIO_RESULTADOS = "resultados/"
DIRECTORIO_IMAGENES = "imagenes/"
RUTA_ESTILO = "../" + DIRECTORIO_ENTRADAS

FICHERO_DATOS_pp     = DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"
FICHERO_DATOS_ca     = DIRECTORIO_ENTRADAS + "comunidadesAutonomas.htm"
FICHERO_DATOS_cap    = DIRECTORIO_ENTRADAS + "comunidadAutonoma-Provincia.htm"
DATOS_LIMPIOS    = DIRECTORIO_ENTRADAS + "poblacionPruebaFinal.csv"


# Funciones lambda para calcular variación absoluta y relativa
variacion_absoluta = lambda actual, anterior: actual - anterior
variacion_relativa = lambda actual, anterior: (variacion_absoluta(actual, anterior) / anterior) * 100

def adjuntarImagen(srcHTML, srcIMG, palabra_a_buscar, dimensiones=(720,720), textAlt="Error al cargar la imagen"):
    """Añade una imagen al HTML
    
    Args:
        srcHTML: Ruta del HTML
        srcIMG: Ruta de la imagen
        palabra_a_buscar: Palabra a buscar en el HTML
        dimensiones: Dimensiones de la imagen. Defaults to (720,720).
        textAlt: Texto alternativo de la imagen. Defaults to "Error al cargar la imagen".

    No duelve nada, modifica el fichero srcHTML
    """
    # Texto para escribir detrás de la palabra encontrada
    texto_html_img = """<img src="%s" alt="%s" width="%s" height="%s">""" % (srcIMG, textAlt, dimensiones[0], dimensiones[1])


    # Abre el archivo en modo lectura y escritura ('r+' para lectura y escritura)
    with open(srcHTML, 'r+') as archivo:
        # Lee el contenido del archivo
        contenido = archivo.read()

        # Encuentra la posición de la palabra en el contenido
        posicion_palabra = contenido.find(palabra_a_buscar)

        # Si la palabra se encuentra en el archivo
        if posicion_palabra != -1:
            # Calcula la posición final de la palabra
            final_palabra = posicion_palabra + len(palabra_a_buscar)

            # Mueve el cursor al final de la palabra
            archivo.seek(final_palabra)

            # Escribe el texto detrás de la palabra
            archivo.write(texto_html_img)

            # Imprime el mensaje de éxito
            print(f"Imagen añadida al fichero {srcHTML}.")

        else:
            print(f"La palabra '{palabra_a_buscar}' no se encontró en el archivo.")

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

def imagenHTML(src, textAlt, dimensiones=(1280,1280)):
    """Crea una imagen HTML

    Args:
        src: Ruta de la imagen
        textAlt: Texto alternativo de la imagen

    Returns:
        imagen: Imagen HTML
    """

    imagen = """<img src="%s" alt="%s" width="%s" height="%s">""" % (src, textAlt, dimensiones[0], dimensiones[1])
    print("Añadida imagen" + src)
    return imagen
def finHTML():
    """Crea el final del fichero HTML

    Returns:
        fin: Final del fichero HTML
    """

    fin = """</body></html>"""

    return fin