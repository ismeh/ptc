cadena = "HoLAA a todos"

print(cadena[0])
# cadena[0] = '' #No se puede asignar
# int(cadena[0]) = int(cadena[0])+32
# int(cadena)

# index_capital_A = cadena[cadena == 'A']
# print(index_capital_A)

index_capital_A = []
for i,letra in enumerate(cadena):
    print(i,letra)
    if letra == 'A':
        index_capital_A.append(i)

print(index_capital_A)

cadena = [l for l in cadena if l != 'A']
print(cadena)