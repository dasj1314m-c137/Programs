# haremos un programa que grafique la funcion 'f(x) = ax² + bx + c', los terminos seran ingresados por el usuario
# ademas calcularemos los intervalos automaticamente obteniendo las coordenadas del vertice y de las raices para ajustar
# para buscar las coordenadas del vertice usaremos '-b / 2a' el cual nos da la coordenada 'x'
# y para obtener la coordenada 'y' aplicamos nuestra funcion con el valor de la coordenada 'x' del vertice
# aunque a nosotros solo nos servira la coordenada 'x'
# con la coordenada x la cual esta en el centrole restamos 5 para calcular el incio del intervalo y sumamos 5 para calcular final intervalo

import numpy as np
import matplotlib.pyplot as plt

# obtenemos terminos de la formula por parte del usuario
a, b, c = float(input("a: ")), float(input("b: ")), float(input("c: "))

# agregamos detalles grafica
plt.style.use("dark_background")
plt.title(f"Graficando f(x) = {round(a)}x² + {round(b)}x + {round(c)}")
plt.xlabel("Intervalo")
plt.grid(True)

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

# mostramos grafica
plt.show()
