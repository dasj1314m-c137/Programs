from math import pi
radio = float(input("Ingresa el radio de la circunferencia: "))
area = pi * (radio**2)
perimetro = 2 * pi * radio
print(f"El perimetro de la circunferencia es: {round(perimetro, 2)} y el area es: {round(area, 2)}")
