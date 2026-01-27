from math import pi, sin
# calculo de area de un triangulo usando dos lados y el angulo entre estos
lados = []
for i in range(2):
    lados.append(float(input(f"Ingrese el valor lado {i + 1}: ")))
grados = float(input("Ingrese el angulo entre los dos lados ingresados: "))
# calculo de radianes usando regla de tres sabiendo que pi radianes son 180 grados
radianes = grados * (pi / 180)
# aplicames formula
area = (lados[0] * lados[1] * sin(radianes)) / 2
# mostramos area
print(f"El area del triangulo es: {area}")
