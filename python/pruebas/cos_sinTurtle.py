import turtle
import numpy as np

n = float(input("Inicio: "))
m = float(input("Final "))

window = turtle.Screen()
window.bgcolor("black")
window.setup(width=800, height=600)
window.setworldcoordinates(n, -2, m, 2)

t = turtle.Turtle()
t.shape("turtle")
t.pensize(5)
t.color("red")

t1 = turtle.Turtle()
t1.shape("turtle")
t1.pensize(5)
t1.color("cyan")

t2 = turtle.Turtle()
t2.shape("turtle")
t2.color("white")
t2.pensize(3)

x_arr = np.linspace(n, m, 100)
# array del seno y coseno
y_arr_sin = np.sin(x_arr)
y_arr_cos = np.cos(x_arr)
# sumamos arrays de coseno y coseno
y_arr_sinCos = y_arr_cos + y_arr_sin

# añadir lineas del plano cartesiano
t2.penup()
t2.goto(n, 0)
t2.pendown()
t2.goto(m, 0)
t2.penup()
t2.goto(((m - n) / 2), 2)
t2.pendown()
t2.goto(((m - n) / 2), -2)

t.penup()
t1.penup()
for i, x in enumerate(x_arr):
    # dibujamos el seno con la primera turtle
    t.goto(x, y_arr_sin[i])
    # dibujamos el coseno con la segunda turtle
    t1.goto(x, y_arr_cos[i])
    # bajamos los lapices luego de que se muevan a sus posiciones primarias
    t1.pendown()
    t.pendown()

window.mainloop()
