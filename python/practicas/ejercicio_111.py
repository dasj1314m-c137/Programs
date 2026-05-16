# en este programa calcularemos permutaciones (el orden importa) usando esta formula
# P(n, m) = n! / (n - m)!
# n representa el numero de elementos posibles y m la cantidad de elementos que queremos
# cuando calculamos n! estamos calculando todas las formas de ordenar todos los elementos
# luego al hacer (n - m)! estamos calculando la cantidad de posiciones que no queremos
# y al dividir estamos cancelando las posiciones extra que no necesitamos osea es un filtro que elimina lo que no queremos
# 5! / (5 - 3)! = 5 * 4 * 3 * 2 * 1 / 2 * 1 entonces el dos y el uno de abajo cancelan a los de arriba y queda
# 5 * 4 * 3 y estos son los que queremos entonces se multiplican y obtenemos solo los que necesitamos

n = int(input("Ingresa el numero de elementos posibles (n): "))
m = int(input("Ingresa el numero elementos que necesitas (m): "))

# funcion para calcular factorial
def factorial(num):
    factorial = 1
    if (num != 0):
        for i in range(1, num + 1):
            factorial *= i
    return factorial

p = factorial(n) / factorial((n - m))

print(f"El numero de permutaciones es: {p}")
