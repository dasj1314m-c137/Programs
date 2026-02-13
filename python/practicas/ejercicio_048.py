import turtle

t = turtle.Turtle()
window = turtle.Screen()

window.setup(width=800, height=800)
window.setworldcoordinates(-200, -200, 1200, 1200)

t.color("black")
t.shape("turtle")
t.pensize(5)

# lista de radios para iterar
radios = [100, 200, 300]

# bucle para iterar sobre los radios de nuestros circulos concentricos
for i, r in enumerate(radios):
    # levantamos el lapiz para dirigirnos al centro
    t.penup()
    # nos dirigimos al centro y del centro bajamos la longitud del radio para centrar el circulo
    t.goto(500, (500 - r))
    # bajamos el lapiz para dibujar
    t.pendown()
    if (i == 0):
        # si es el primer circulo lo rellenamos
        t.begin_fill()
        t.circle(r)
        t.end_fill()
        continue
    t.circle(r)

# dibujar las dos lineas que atraviesan los circulos concentricos
t.goto(500, 0)
t.goto(500, 1000)
t.penup()
t.goto(0, 500)
t.pendown()
t.goto(1000, 500)

# diccionario con las letras y sus coordenadas correspondientes
letters = {
    'a': (500, 700),
    'b': (700, 500),
    'c': (500, 300),
    'd': (300, 500)
}

t.penup()
# recorremos bucle for para dirigirnos a las coordenadas de las letras y dibujarlas
for key, value in letters.items():
    t.goto(value[0], value[1])
    t.write(key, font=("Arial", 25, "bold"))

window.mainloop()
