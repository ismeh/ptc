# -*- coding: utf-8 -*-

from tkinter import *
import parametros as p

def onClickConectarSim():
    print("onClickConectarSim")
    p.textLabelEstado = "Estado: Conectado con CoppeliaSim"


def onClickDetenerSim():
    print("onClickDetenerSim")

def onClickCapturar():
    print("onClickCapturar")

def onClickAgrupar():
    print("onClickAgrupar")

def onClickExtraerCaracteristicas():
    print("onClickExtraerCaracteristicas")

def onClickEntrenarClasificador():
    print("onClickEntrenarClasificador")

def onClickPredecir():
    print("onClickPredecir")

def onClickSalir():
    print("onClickSalir")

def onClickCambiar():
    print("onClickCambiar")
    p.val_iteraciones = int(entryIter.get())
    p.val_cerca = float(entryCerca.get())
    p.val_media = float(entryMedia.get())
    p.val_lejos = float(entryLejos.get())
    p.val_minPuntos = int(entryMinPuntos.get())
    p.val_maxPuntos = int(entryMaxPuntos.get())
    p.val_umbralDistancia = float(entryUmbralDistancia.get())


def onClickDebug(listaBotones):
    print("onClickDebug")
    activarBotones(listaBotones)

def desactivarBotones(listaBotones):
    for boton in listaBotones:
        boton.config(state=DISABLED)

def activarBotones(listaBotones):
    for boton in listaBotones:
        boton.config(state=NORMAL)

def main():
    r = 0 #Fila actual
    c = 0 #Columna actual
    global entryIter, entryCerca, entryMedia, entryLejos, entryMinPuntos, entryMaxPuntos, entryUmbralDistancia
    width_entry_box = 6

    root = Tk()
    root.geometry("700x300")
    root.title("Práctica PTC Tkinter Robótica")

    #Columna 0
    labelInicial = Label(root, text="Es necesario ejecutar el simulador CoppeliaSim")
    labelInicial.grid(row=r, column=c)
    r += 1

    btnConectarSim = Button(root, command=onClickConectarSim, text="Conectar con CoppeliaSim")
    btnConectarSim.grid(row=r, column=c)
    r += 1

    btnDetenerSim = Button(root, command=onClickDetenerSim, text="Detener y desconectar CoppeliaSim")
    btnDetenerSim.grid(row=r, column=c)
    r += 1

    labelEstado= Label(root, text=p.textLabelEstado)
    labelEstado.grid(row=r, column=c)
    r += 1

    btnCapturar = Button(root, command=onClickCapturar, text="Capturar")
    btnCapturar.grid(row=r, column=c)
    r += 1

    btnAgrupar = Button(root, command=onClickAgrupar, text="Agrupar")
    btnAgrupar.grid(row=r, column=c)
    r += 1

    btnExtraerCaracteristicas = Button(root, command=onClickExtraerCaracteristicas, text="Extraer características")
    btnExtraerCaracteristicas.grid(row=r, column=c)
    r += 1

    btnEntrenarClasificador = Button(root, command=onClickEntrenarClasificador, text="Entrenar clasificador")
    btnEntrenarClasificador.grid(row=r, column=c)
    r += 1

    btnPredecir = Button(root, command=onClickPredecir, text="Predecir")
    btnPredecir.grid(row=r, column=c)
    r += 1

    btnSalir = Button(root, command=onClickSalir, text="Salir")
    btnSalir.grid(row=r, column=c)
    r += 1

    btnDebug = Button(root, command=onClickDebug, text="Debug")
    btnDebug.grid(row=r, column=c)
    r += 1

    #Columna 1 y 2
    r=1
    c=1
    labelParam = Label(root, text="Parámetros")
    labelParam.grid(row=r, column=c, sticky='e')
    r += 1

    labelIter = Label(root, text="Iteraciones:")
    labelIter.grid(row=r, column=c, sticky='e')
    entryIter = Entry(root, width=width_entry_box)
    entryIter.insert(0, p.val_iteraciones.__str__())
    entryIter.grid(row=r, column=c+1)

    r += 1
    labelCerca = Label(root, text="Cerca:")
    labelCerca.grid(row=r, column=c, sticky='e')
    entryCerca = Entry(root, width=width_entry_box)
    entryCerca.insert(0, p.val_cerca.__str__())
    entryCerca.grid(row=r, column=c+1)

    r += 1
    labelMedia = Label(root, text="Media:")
    labelMedia.grid(row=r, column=c, sticky='e')
    entryMedia = Entry(root, width=width_entry_box)
    entryMedia.insert(0, p.val_media.__str__())
    entryMedia.grid(row=r, column=c+1)

    r += 1
    labelLejos = Label(root, text="Lejos:")
    labelLejos.grid(row=r, column=c, sticky='e')
    entryLejos = Entry(root, width=width_entry_box)
    entryLejos.insert(0, p.val_lejos.__str__())
    entryLejos.grid(row=r, column=c+1)

    r += 1
    labelMinPuntos = Label(root, text="MinPuntos:")
    labelMinPuntos.grid(row=r, column=c, sticky='e')
    entryMinPuntos = Entry(root, width=width_entry_box)
    entryMinPuntos.insert(0, p.val_minPuntos.__str__())
    entryMinPuntos.grid(row=r, column=c+1)

    r += 1
    labelMaxPuntos = Label(root, text="MaxPuntos:")
    labelMaxPuntos.grid(row=r, column=c, sticky='e')
    entryMaxPuntos = Entry(root, width=width_entry_box)
    entryMaxPuntos.insert(0, p.val_maxPuntos.__str__())
    entryMaxPuntos.grid(row=r, column=c+1)

    r += 1
    labelUmbralDistancia = Label(root, text="UmbralDistancia:")
    labelUmbralDistancia.grid(row=r, column=c, sticky='e')
    entryUmbralDistancia = Entry(root, width=width_entry_box, text=p.val_umbralDistancia.__str__())
    entryUmbralDistancia.insert(0, p.val_umbralDistancia.__str__())
    entryUmbralDistancia.grid(row=r, column=c+1)

    r += 1
    btnCambiar = Button(root, command=onClickCambiar, text="Cambiar")
    btnCambiar.grid(row=r, column=c)

    #Columna 3
    r=1
    c=3

    labelFicheros = Label(root, text="Ficheros para la captura")
    labelFicheros.grid(row=r, column=c)
    r += 2

    # root.grid_rowconfigure(r, weight=0)
    listboxFicheros = Listbox(root, width=35, height=12)
    listboxFicheros.grid(row=r, column=c, rowspan=6)

    #Añadir entradas a listboxFicheros
    listaFicheros = ["positivo1/enPieCerca.json", "positivo2/enPieMedia.json", "positivo3/enPieLejos.json",
                     "positivo4/sentadoCerca.json", "positivo5/sentadoMedia.json", "positivo6/sentadoLejos.json",
                     "negativo1/cilindroMenorCerca.json", "negativo2/cilindroMenorMedia.json", "negativo3/cilindroMenorLejos.json",
                     "negativo4/cilindroMayorCerca.json", "negativo5/cilindroMayorMedia.json", "negativo6/cilindroMayorLejos.json"]

    for fichero in listaFicheros:
        listboxFicheros.insert(END, fichero)

    desactivarBotones([btnDetenerSim, btnCapturar, btnAgrupar, btnExtraerCaracteristicas, btnEntrenarClasificador, btnPredecir])
    # print(btnAgrupar.config().keys())

    root.mainloop() #Event Listener, Bucle infinito



main()