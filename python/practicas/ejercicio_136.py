# from math import sin, pi
# para obtener el cosenos hay dos metodos utiles que podemos utilizar
# hipotenusa = 8

# en el primer metodo utilizamos la funcion del seno donde le pasamos radianes y este con las series de Taylor calcula el seno
# radianes = 30 * (pi / 180)
# func_sin = sin(radianes)

# el segundo metodo debemos dividir el cateto opuesto entre la hipotenusa
# para obtener la longitud del cateto opuesto podemos multiplicar el resultado del seno por la hipotenusa
# cateto_opuesto_a = func_sin * hipotenusa
# a_b_sin = cateto_opuesto_a / hipotenusa

# print(f"El seno usando funcion: {func_sin}")
# print(f"Longitud del cateto opuesto 'a': {cateto_opuesto_a}")
# print(f"El seno dividiendo cateto opuesto entre hipotenusa {a_b_sin}")

# el seno representa la coordenada y en el circulo unitario

# al igual que con el coseno al momento de graficar el seno debemos aplicar el seno a la coordenada 'y' porque esta es la cambiante
# mientras que la coordenada 'x' se queda con los radianes los cuales representan la progresion, siempre va adelante

import numpy as np
import matplotlib.pyplot as plt

# pedimos input rango de valores para crear las coordenadas
n = float(input("Ingresa el incio del limite en radianes: "))
m = float(input("Ingresa el final del limite en radianes: "))

# creamos coordenadas x como espacios igualmente espaciados con linspace en el rango que el usuario ingreso
x_array = np.linspace(n, m, 100)

# creamos coordenadas y aplicando el seno a los radianes
y_array = np.sin(x_array)

# agregamos d etalles a la grafica
plt.style.use("dark_background")
plt.title("Graficamos seno")
plt.xlabel("Datos de progresion, radianes")
plt.ylabel("Datos de cambio, seno")
plt.grid(True)

# graficamos el seno
plt.plot(x_array, y_array)

# mostramos grafica
plt.show()
