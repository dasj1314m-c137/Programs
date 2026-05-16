num = int(input("Ingrese el numero: "))
factorial = 1

if (num != 0):
    for i in range(1, num + 1):
        factorial *= i

print(f"El factorial de {num} es: {factorial}")
