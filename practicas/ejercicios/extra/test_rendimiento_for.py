import time

n = 100000000
print ("Creando una lista con", n, "valores usando compresión de listas")
t1 = time.time();
v = [ 2+i*12 for i in range(n) ];
t2 = time.time();
tiempo1 = t2-t1
print("Tiempo invertido:", tiempo1)

print ("Creando una lista con", n, "valores sin usar compresión de listas")
t1 = time.time();
v = []
for i in range(n) :
    v.append(2+i*12)
t2 = time.time()
tiempo2 = t2-t1
print("Tiempo invertido:", tiempo2)

print("\nDiferencia de tiempo: ", abs(tiempo1 - tiempo2), "segundos")