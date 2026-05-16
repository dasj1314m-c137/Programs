# en este programa calcularemos distancias entre coordenadas x, y
# para eso usaremos el teorema de Pitagoras
# nos permite saber la longitud de la hipotenusa la cual es la raiz de la suma de los cuadrados de sus catetos
# entonces sus catetos en este caso seran la resta entre las coordenadas que deseamos medir su distancia
# restar nos sirve para obtener la longitud de los catetos que se forman entre las coordenadas

coordenadas = []
distancias = []

for i in range(5):
    print(f"Ingresa las coordenadas del punto {i + 1}")
    x, y = float(input("x: ")), float(input("y: "))
    coordenadas.append((x, y))

for i, x_y in enumerate(coordenadas):
    if (i != 0):
        d = (((coordenadas[0][0] - x_y[0])**2) + ((coordenadas[0][1] - x_y[1])**2)) ** (1 / 2)
        distancias.append(d)

low_d = min(distancias)
i_low_d = distancias.index(low_d)

print(f"El punto mas cercano es el {i_low_d + 2} a una distancia de {round(low_d, 4)}")
