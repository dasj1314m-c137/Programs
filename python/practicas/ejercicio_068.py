amount = int(input("Ingresa la cantidad de pesos: "))
billetes = [500, 200, 100, 50, 20, 10, 5, 2, 1]

for billete in billetes:
    if (amount != 0 and billete <= amount):
        cant_billetes = amount // billete
        amount = amount % billete
        print(f"{cant_billetes} de {billete}")
