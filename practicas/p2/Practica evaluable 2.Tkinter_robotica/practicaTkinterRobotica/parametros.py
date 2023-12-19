# -*- coding: utf-8 -*-
from enum import Enum

#Enumerado para el estado del programa
class Estado(Enum):
    desconectado = 0
    conectado = 1

textLabelEstado = "Estado: ---"
val_iteraciones = 50
val_cerca = 0.5
val_media = 1.5
val_lejos = 2.5
val_minPuntos = 0 #0 Mínimo número de puntos para considerar un cluster
val_maxPuntos = 0 #0 Máximo número de puntos en un cluster, 40 debido a que en el ciclindro grande al ponerlo cerca se capturan 76 por eso puse máx 40
val_umbralDistancia = 0 #0 Si la distancia entre dos puntos es menor que este valor se consideran del mismo cluster
estado = Estado.desconectado
clientID = -1

longitud_output = 33

debug_directorios = False
