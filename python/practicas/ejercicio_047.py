import turtle

t = turtle.Turtle()
ventana = turtle.Screen()
ventana.setup(width=800, height=800)
ventana.setworldcoordinates(-200, -200, 1200, 1200)

t.color("red")
t.shape("turtle")
t.pensize(5)

# creamos lista para almacenar los radios de los circulos concentricos
radio_circulos = [100, 200, 300]

# creamos bucle for que itera sobre la lista de radios y usamos enumerate para obtener su indice lo que nos permitira crear cada uno
for i, radio in enumerate(radio_circulos):
    t.penup()
    # nos dirigimos al centro sin dibujar, pero en la coordenada y bajamos de la mitad menos el radio para que todos los circulos esten alineados
    t.goto(500, (500 - radio))
    t.pendown()
    # checamos indice para que solo el primer circulo sea rellenado
    if i == 0:
        t.begin_fill()
        t.circle(radio)
        t.end_fill()
    # para los demas circulos solo trazar la circunferencia
    else:
        t.circle(radio)

# bucle en rango de dos para crear la linea vertical y horizontal que atraviezan los circulos formando la cruz
for i in range(2):
    t.penup()
    # condicionales la primera revisa si es la primera iteracion y viaja sin trazar hasta el centro pero en la coordenada x mas a la derecha
    if i == 0:
        t.goto((500 - 500), 500)
    # si no es la primera iteracion ejecutamos esta que viaja sin trazar al centro pero en la coordenada y mas abajo y giramos para orientar arriba
    else:
        t.goto(500, (500 - 500))
        t.setheading(90)
    # preparamos para dibujar y avanzamos mil coordenadas hacia adelante lo suficiente para atravezar los 3 circulos
    t.pendown()
    t.forward(1000)

ventana.mainloop()
