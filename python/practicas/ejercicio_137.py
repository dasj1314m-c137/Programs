# from math import cos, pi
# para calcular el coseno hay dos metodos, los cuales son los siguientes
# hipotenusa = 10

# en el primer metodo usamos la funcion del coseno donde le pasamos los radianes para que lo calcule usando las series de Taylor
# radianes = 30 * (pi / 180)
# func_cos = cos(radianes)

# en el segundo metodo dividimos el cateto adyacente 'b' entre la hipotenusa
# tambien para averiguar el valor del cateto adyacente podemos multiplicar la hipotenusa por el valor del coseno
# cateto_adyacente_b = hipotenusa * func_cos
# b_h_cos = cateto_adyacente_b / hipotenusa

# print(f"Coseno desde funcion cos {func_cos}")
# print(f"El cateto adyacente es: {cateto_adyacente_b}")
# print(f"Coseno desde division de cateto adyacente entre hipotenusa {b_h_cos}")

# el coseno representa la coordenada x en el circulo unitario

# para graficar la coordenada 'x' son los radianes y la coordenada 'y' es el resultado del coseno aplicado a los radianes
# hacemos esto porque la coordenada x representa la progresion, simpre va adelante no cambia
# entonces por eso aplicamos el coseno en y porque este si cambia sube o baja

import numpy as np
import matplotlib.pyplot as plt

n = float(input("Ingresa el incio del limite en radianes: "))
m = float(input("Ingresa el final del limite en radianes: "))

# crear array de las coordenadas 'x' con los radianes
# linspace crea un array igualmente espaciado entre los rangos especificados
x_arr = np.linspace(n, m, 100)
# crear array de las coordenadas 'y' con el resultado del coseno sobre los radianes
y_arr = np.cos(x_arr)

# añadimos detalles a la grafica
plt.style.use("dark_background")
plt.title("Graficamos el coseno")
plt.xlabel("Datos de progresion, radianes")
plt.ylabel("Datos de cambio, coseno")
plt.grid(True)

# graficamos las ondas usando matplot
plt.plot(x_arr, y_arr)

# mostrar grafica
plt.show()

# print("Array de las coordenadas x")
# print(x_arr)
# print("Array de las coordenadas y")
# print(y_arr)
