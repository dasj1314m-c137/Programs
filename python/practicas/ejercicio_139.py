# crearemos un array entre el intervalo de -2 a 2 esto seran nuestrar coordenadas x
# para las coordenadas y (cambiantes) aplicaremos a todos la formula '1 / (x + 1)'
# pero hay una excepcion si 'x' es igual a '-1' la operacion quedaria asi '1 / 0' lo cual no puede ser
# entonces antes de aplicar la formula debemos eliminar '-1' del array primario
# luego de graficar la funcion '1 / (x + 1)' sin el '-1' vamos a graficar el '-1' en las coordenadas '(-1, 0)' con otro color
# ademas me di cuenta que igual los numeros mas cercanos a '-1' al momento de dividir a '1' el valor crece demasiado

import numpy as np
import matplotlib.pyplot as plt

# para excluir los valores cercamos a '-1' creremos dos arrays con rangos que excluyan el '-1' y cercanos
# creamos 50 puntos (coordenadas x) en el intervalo entre -0.9 y 2, empieza 1 decima antes del -1
x_arr_der = np.linspace(-0.9, 2, 50)
# creamos 50 puntos (coordenadas x) en el intervalo entre -2 y -1.1, termina 1 decima antes del -1
x_arr_izq = np.linspace(-2, -1.1, 50)

# creamos coordenada y aplicando la formula '1 / (x + 1)' a todos los elementos de x_arr
y_arr_der = 1 / (x_arr_der + 1)
y_arr_izq = 1 / (x_arr_izq + 1)

# agregamos detalles a la grafica
plt.style.use("dark_background")
plt.title("Graficamos '1 / (x+1)' en intervalo de '[-2, 2]'")
plt.xlabel("Datos de progresion, intervalo '[-2, 2]'")
plt.ylabel("Datos cambiantes, formula '1 / (x+1)'")
plt.grid(True)

# graficamos la formula
plt.scatter(x_arr_der, y_arr_der, color="cyan", s=100)
plt.scatter(x_arr_izq, y_arr_izq, color="cyan", s=100)

# graficamos el punto de -1 en las coordenadas (-1, 0)
plt.scatter([-1], [0], color="red", s=100)

# mostramos grafica
plt.show()
