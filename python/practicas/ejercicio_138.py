# para este programa graficaremos el seno y el coseno con diferentes colores
import numpy as np
import matplotlib.pyplot as plt

n = float(input("Ingresa el inicio del limite en radianes: "))
m = float(input("Ingresa el final del limite en radianes: "))

# creamos 100 puntos (coordenadas x) igualmente espaciados entre el rango de radianes ingresado por el usuario
x_arr = np.linspace(n, m, 100)
# creamos coordenadas y del coseno
y_cos = np.cos(x_arr)
# creamos coordenadas y del seno
y_sin = np.sin(x_arr)

# añadimos detalles
plt.style.use("dark_background")
plt.title("Graficamos seno y coseno")
plt.xlabel("Datos de progresion, radianes")
plt.ylabel("Datos cambiantes, seno y coseno")
plt.grid(True)

# graficamos coseno
plt.plot(x_arr, y_cos, color="cyan", label="coseno")
# graficamos seno
plt.plot(x_arr, y_sin, color="red", label="seno")

# mostrar etiqueta leyendas
plt.legend()

# mostramos grafica
plt.show()
