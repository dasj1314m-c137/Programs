import math
# formula de heron para calcular area de un triangulo usando solo sus tres lados
lados = []
for i in range(3):
    lados.append(float(input(f"Ingrese el valor de lado {i + 1}: ")))
# calculamos perimetro
perimetro = sum(lados)
# calculo del semipermietro donde dividimos el perimetro entre dos
s = perimetro / 2
# aplicamos formula de heron donde le restamos al semiperimetro cada lado
# y luego multiplicamos todos los valores restantes y tambien el semiperimetro
# al final guardamos los resultados en la var area y sacamos la raiz
area = s
for lado in lados:
    area *= s - lado
area = math.sqrt(area)
# mostramos resultados
print(f"El perimetro del triangulo es: {perimetro} y el area es: {area}")
