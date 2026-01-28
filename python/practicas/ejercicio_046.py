import turtle
# crear objeto turtle y la ventana
t = turtle.Turtle()
window = turtle.Screen()
window.setup(width=800, height=800)
# ajustamos las coordenadas que muestra para poder acceder a la cordenada 900, 900
window.setworldcoordinates(-200, -200, 1200, 1200)
# ajustamos detalles de nuestra tortuga
t.color("red")
t.pensize(5)
t.shape("turtle")
# dejamos de dibujar y posicionamos la tortuga en la esquina inferior izquierda para poder empezar a dibujar
t.penup()
t.goto(100, 100)
t.pendown()
# creamos un bucle for que crea el cuadrado
# donde la tortuga avanza hasta la coordenada x 900, luego giramos un angulo de 90° y asi repite hasta terminar
for i in range(4):
    t.forward(800)
    t.left(90)
# como terminamos en la coordenada 100, 100 hacemos que la tortuga avanze de forma diagonal a la otra esquina
t.goto(900, 900)
# dejamos de dibujar y colocamos a la tortuga en la esquina superior izquierda para dibujar la ultima diagonal
t.penup()
t.goto(100, 900)
t.pendown()
# una vez habiendo movido la tortuga la la esquina correspondiente apuntamos y trazamos hacia a la esquina opuesta
t.goto(900, 100)

window.mainloop()
