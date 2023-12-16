# -*- coding: utf-8 -*-
import os.path
# import sim #Para ubuntu
import sim #Para windows
import sys
from tkinter import *
from tkinter import messagebox

import parametros as p
import capturar
import agrupar

def main():
    def crearDirectorios():
        for i in range(1, 7):
            os.makedirs("negativo" + str(i), exist_ok=True)
            os.makedirs("positivo" + str(i), exist_ok=True)

        os.makedirs("prediccion", exist_ok=True)
        print("Directorios creados")
    def onClickConectarSim():
        sim.simxFinish(-1)  # Terminar todas las conexiones
        p.clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000,
                                  5)  # Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)

        if p.clientID != -1:
            print('Conexion establecida')
            btnCapturar.config(state=NORMAL)
            btnDetenerSim.config(state=NORMAL)
        else:
            sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.")
        p.textLabelEstado = "Estado: Conectado con CoppeliaSim"
        p.estado = p.Estado.conectado


    def onClickDetenerSim():
        # detenemos la simulacion
        sim.simxStopSimulation(p.clientID, sim.simx_opmode_oneshot_wait)

        # cerramos la conexion
        sim.simxFinish(p.clientID)

        btnCapturar.config(state=DISABLED)
        btnDetenerSim.config(state=DISABLED)
        p.textLabelEstado = "Estado: Desconectado de CoppeliaSim"
        messagebox.showinfo("Práctica PTC Tkinter Robótica",
                            "Se ha detenido la simulación y se ha desconectado de CoppeliaSim")
        p.estado = p.Estado.desconectado

    def onClickCapturar():
        fichero = listboxFicheros.get(ANCHOR)

        if fichero == "":
            messagebox.showwarning("Práctica PTC Tkinter Robótica", "Debe elegir un fichero de la lista")
        else:
            # Comprobar existencia del fichero
            if os.path.exists(fichero):
                if messagebox.askyesno("Práctica PTC Tkinter Robótica",
                                    f"El fichero: {fichero} ya existe. Se creará de nuevo. ¿Está seguro?"):
                    capturar.main(fichero)
                    btnAgrupar.config(state=NORMAL)

            else:
                if messagebox.askyesno("Práctica PTC Tkinter Robótica",
                                    f"Se va a crear el fichero: {fichero} ¿Está seguro?"):
                    capturar.main(fichero)
                    btnAgrupar.config(state=NORMAL)


    def onClickAgrupar():
        print("onClickAgrupar")
        agrupar.main()
        btnExtraerCaracteristicas.config(state=NORMAL)

    def onClickExtraerCaracteristicas():
        print("onClickExtraerCaracteristicas")
        #.main()
        btnEntrenarClasificador.config(state=NORMAL)

    def onClickEntrenarClasificador():
        # .main()
        btnPredecir.config(state=NORMAL)
        print("onClickEntrenarClasificador")

    def onClickPredecir():
        # .main()
        print("onClickPredecir")

    def onClickSalir():
        if p.estado == p.Estado.conectado:
            messagebox.showwarning("Práctica PTC Tkinter Robótica",
                                   "Debe detener la simulación y desconectar de CoppeliaSim antes de salir")
        else:
            if messagebox.askyesno("Práctica PTC Tkinter Robótica", "¿Está seguro de que desea salir?"):
                sys.exit("Cerrando interfaz")

    def onClickCambiar():
        p.val_iteraciones = int(entryIter.get())
        p.val_cerca = float(entryCerca.get())
        p.val_media = float(entryMedia.get())
        p.val_lejos = float(entryLejos.get())
        p.val_minPuntos = int(entryMinPuntos.get())
        p.val_maxPuntos = int(entryMaxPuntos.get())
        p.val_umbralDistancia = float(entryUmbralDistancia.get())

        print(p.val_iteraciones)
        print(p.val_cerca)
        print(p.val_media)
        print(p.val_lejos)
        print(p.val_minPuntos)
        print(p.val_maxPuntos)
        print(p.val_umbralDistancia)

    def onClickDebug():
        activarBotones()

    def desactivarBotones(listaBotones):
        for boton in listaBotones:
            boton.config(state=DISABLED)

    def activarBotones():
        listaBotones = [btnDetenerSim, btnCapturar, btnAgrupar, btnExtraerCaracteristicas, btnEntrenarClasificador,
                        btnPredecir]
        for boton in listaBotones:
            boton.config(state=NORMAL)

    r = 0 #Fila actual
    c = 0 #Columna actual
    width_entry_box = 6

    root = Tk()
    root.geometry("700x320") #300
    root.title("Práctica PTC Tkinter Robótica")
    crearDirectorios()

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