num = float(input("Ingresa un numero: "))

for i in range(2, 101):
    raiz_n_esimas = num ** (1 / i)
    print(f"La raiz {i}-esima es: {round(raiz_n_esimas, 4)}")
