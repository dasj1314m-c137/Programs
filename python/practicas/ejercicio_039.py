cantidad_euros = float(input("Ingresa la cantidad de euros: "))
tasa_interes = float(input("Ingresa la tasa de interes: "))
num_años = int(input("Ingresa la numero de años: "))

capital_final = cantidad_euros * (1 + tasa_interes / 100)**num_años
print(f"La capital final de {cantidad_euros} con una tasa de interes del {tasa_interes} por {num_años} años es: {round(capital_final, 2)}")
