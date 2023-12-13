import random
import time

from matplotlib import pyplot as plt


def grafica(x, y, y1, tittle, y_label="Tiempo (segundos)", x_label="Número de elementos", legends=["Compresión", "Sin compresión"]):
    plt.title(tittle)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.plot(x, y, "og-")
    plt.plot(x, y1, "or-")
    plt.legend(legends)
    plt.grid()
    plt.show()

print("Test de rendimiento para creación de listas")
v=0
n = [100000, 1000000, 10000000, 50000000, 100000000, 200000000] #grande
n_peque = [1000, 5000, 10000, 15000, 20000] #pequeño
# resultados1 = []
# for valores in n:
#     t1 = time.time()
#     v = [ 2+i*12 for i in range(valores)]
#     t2 = time.time()
#     tiempo1 = t2-t1
#     resultados1.append(tiempo1)
#
# print("Usando compresión de listas: ", resultados1) #Arriba

#Sin compresión de listas abajo
resultados2 = []
for valores in n:
    t1 = time.time()
    v = []
    for i in range(valores) :
        v.append(2+i*12)
    t2 = time.time()
    tiempo1 = t2-t1
    resultados2.append(tiempo1)

print("Tiempos Sin usar compresión de listas: ", resultados2)


print("Test de rendimiento para algoritmo de ordenación (burbuja)")
resultados3 = []

def bubble_sort(lista):
    n = len(lista)

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                # Intercambiar elementos si están en el orden incorrecto
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

for valores in n_peque:
    lista = random.sample(range(1,valores+1), valores)
    t1 = time.time()
    bubble_sort(lista)
    t2 = time.time()
    tiempo1 = t2-t1
    resultados3.append(tiempo1)

print("Tiempos de ordenación (burbuja): ", resultados3)



# datos_pypy = [0.0009999275207519531, 0.009999990463256836, 0.1099998950958252, 0.5, 1.0]
# datos_python = [0.013998985290527344, 0.16101312637329102, 1.5880699157714844, 7.982882261276245, 16.42805790901184]
# grafica(n, datos_python, datos_pypy,"Rendimiento creación de listas", legends=["Python", "PyPy"])
grafica(n_peque, resultados3, resultados3,"Rendimiento ordenar", legends=["Python", "PyPy"])

###Codigo antiguo del profesor -------------------


# n = 100000000
# print ("Creando una lista con", n, "valores usando compresión de listas")
# t1 = time.time();
# v = [ 2+i*12 for i in range(n) ];
# t2 = time.time();
# tiempo1 = t2-t1
# print("Tiempo invertido:", tiempo1)
#
# print ("Creando una lista con", n, "valores sin usar compresión de listas")
# t1 = time.time();
# v = []
# for i in range(n) :
#     v.append(2+i*12)
# t2 = time.time()
# tiempo2 = t2-t1
# print("Tiempo invertido:", tiempo2)
#
# print("\nDiferencia de tiempo: ", abs(tiempo1 - tiempo2), "segundos")