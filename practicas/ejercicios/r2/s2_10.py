"""
10. Partiendo de una disolución de ácido sulfúrico en agua al 80 % de concentración, quiero obtener
una cantidad x de centímetros cúbicos a una concentración y% (y<80%). Siendo x, e y valores de
entrada al programa, calcular cuantos centímetros cúbicos de la disolución al 80% y de agua son
necesarios para obtener los x centímetros cúbicos deseados al y% de concentración.
"""
CONCENTRACION_INICIAL = 0.8
x = volumen_final = float(input("Cantidad de disolución a obtener: "))
y = concentracion_final = float(input("Porcentaje de concentracion deseado: ")) / 100

volumen_inicial = x * y / CONCENTRACION_INICIAL
agua_necesaria = x - volumen_inicial

print("Para un volumen final(x) de ", x, "cc y una concentración final (y)", y,
      "necesitamos un volumen inicial de disolución de", volumen_inicial, "cc y", agua_necesaria, "cc de agua")
