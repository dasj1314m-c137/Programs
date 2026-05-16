num1 = int(input("Ingresa un numero entero: "))
num2 = int(input("Ingresa un numero entero: "))

nums_sqrt = [num1**2, num2**2]

if (nums_sqrt[0] == nums_sqrt[1]):
    print("El segundo es el cuadrado exacto del primero")
elif (nums_sqrt[0] < nums_sqrt[1]):
    print("El segundo es mayor que el cualdrado del primero")
else:
    print("El segundo es menor que el cuadrado del primero")
