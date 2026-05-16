# para este programa calcularemos combinaciones (el orden no importa) usando esta formula:
# C(n, m) = P(n, m) / m!
# n representa el total de elementos posibles y m cuantos elementos queremos
# esta formula usa la formula de permutaciones en su interior y al final solo divide el resultado por m factorial
# m! representa lo que queremos queremos pero tambien este nos ayuda a eliminar
# las repeticiones de los diferentes grupos obtenidos por eso dividimos (filtramos) para eliminar las repeticiones

n = int(input("Ingresa el valor de n: "))
m = int(input("Ingresa el valor de m: "))

def factorial(num):
    factorial = 1
    if (num != 0):
        for i in range(1, num + 1):
            factorial *= i
    return factorial

c = (factorial(n) / factorial((n - m))) / factorial(m)

print(f"El numero de combinaciones posibles es: {c}")
