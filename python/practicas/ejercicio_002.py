bits = 1
valor_maximo = 1
userNum = int(input("Ingresa el numero y te diremos con cuantos bits se representa: "))

while userNum > valor_maximo:
    bits += 1
    valor_maximo = (2**bits) - 1

print(f"Para representar el numero {userNum} se necesitan {bits} bits")