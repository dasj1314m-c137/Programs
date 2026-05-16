# en este programa añadiremos, puntos rojos en las raices de la parabola
import math
import numpy as np
import matplotlib.pyplot as plt

# obtenemos terminos de la formula por parte del usuario
a, b, c = float(input("a: ")), float(input("b: ")), float(input("c: "))

# agregamos detalles grafica
plt.style.use("dark_background")
plt.title(f"Graficando f(x) = {round(a)}x² + {round(b)}x + {round(c)}")
plt.xlabel("Intervalo")
plt.grid(True)

# coordenadas x de las raices
raices_x = []

# calculamos discriminante
d = (b**2) - 4 * (a * c)
# revisamos si el resultado del discriminante es 0
if (d == 0):
    raices_x.append(-(b) / (2 * a))
# revisamos si el resultado del discriminante es mayor que 0 (no negativo)
elif (d > 0):
    raices_x.append((-(b) + math.sqrt(d)) / (2 * a))
    raices_x.append((-(b) - math.sqrt(d)) / (2 * a))
else:
    print("No hubo raiz")

# coordenadas y de las raices
raices_x = np.array(raices_x)
raices_y = (a * (raices_x ** 2)) + (b * raices_x) + c

# obtenemos coordenada x del vertice
x_vertice = -(b) / (2 * a)
# calculamos intervalos
n, m = (x_vertice - 5), (x_vertice + 5)

# obtenemos coordenadas 'x' y 'y' de nuestra grafica
x = np.linspace(n, m, 100)
y = (a * (x ** 2)) + (b * x) + c

# obtenemos limites de la coordenada y para la grafica
min_y = y.min()
max_y = y.max()
# calculamos margen
margen = (max_y - min_y) * 0.1
# ajustamos los limites de la grafica
plt.ylim(min_y - margen, max_y + margen)

# graficamos parabola
plt.plot(x, y, color="cyan")

# graficamos puntos en las raices
plt.scatter(raices_x, raices_y, s=40, c="red")

# mostramos grafica
plt.show()
