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
val_minPuntos = 3 #0
val_maxPuntos = 5 #0
val_umbralDistancia = 0.3 #0
estado = Estado.desconectado
clientID = -1

longitud_output = 33


